"""
Gemini LLM client with retry logic and error handling.

This module provides a robust client for Google Gemini API integration
with proper error handling, rate limiting, and retry mechanisms.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.env import settings


class GeminiModel(Enum):
    """Available Gemini models."""
    GEMINI_PRO = "gemini-1.5-pro"
    GEMINI_FLASH = "gemini-1.5-flash"


class GeminiError(Exception):
    """Base exception for Gemini API errors."""
    pass


class GeminiRateLimitError(GeminiError):
    """Rate limit exceeded error."""
    pass


class GeminiAPIError(GeminiError):
    """General API error."""
    pass


@dataclass
class GeminiResponse:
    """Response from Gemini API."""
    content: str
    model: str
    usage: Dict[str, Any]
    success: bool
    error: Optional[str] = None


class GeminiClient:
    """Client for Google Gemini API with retry logic and error handling."""
    
    def __init__(self, api_key: Optional[str] = None, model: GeminiModel = GeminiModel.GEMINI_PRO):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Gemini API key, uses settings if None
            model: Gemini model to use
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Setup session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        self.logger = logging.getLogger(__name__)
    
    def _make_request(self, endpoint: str, payload: Dict[str, Any]) -> GeminiResponse:
        """
        Make a request to the Gemini API.
        
        Args:
            endpoint: API endpoint
            payload: Request payload
            
        Returns:
            GeminiResponse object
            
        Raises:
            GeminiRateLimitError: If rate limit exceeded
            GeminiAPIError: If API request fails
        """
        url = f"{self.base_url}/{endpoint}?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        try:
            self.logger.info(f"Making request to Gemini API: {endpoint}")
            response = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 429:
                raise GeminiRateLimitError("Rate limit exceeded")
            
            if not response.ok:
                error_msg = f"API request failed: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                raise GeminiAPIError(error_msg)
            
            data = response.json()
            
            # Extract content from Gemini response
            if "candidates" in data and data["candidates"]:
                candidate = data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    content = candidate["content"]["parts"][0].get("text", "")
                else:
                    content = ""
            else:
                content = ""
            
            # Extract usage information
            usage = data.get("usageMetadata", {})
            
            return GeminiResponse(
                content=content,
                model=self.model.value,
                usage=usage,
                success=True
            )
            
        except requests.exceptions.Timeout:
            error_msg = "Request timeout"
            self.logger.error(error_msg)
            return GeminiResponse(
                content="",
                model=self.model.value,
                usage={},
                success=False,
                error=error_msg
            )
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            self.logger.error(error_msg)
            return GeminiResponse(
                content="",
                model=self.model.value,
                usage={},
                success=False,
                error=error_msg
            )
    
    def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> GeminiResponse:
        """
        Generate text using Gemini API.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            
        Returns:
            GeminiResponse object
        """
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topP": 0.8,
                "topK": 10
            }
        }
        
        endpoint = f"models/{self.model.value}:generateContent"
        return self._make_request(endpoint, payload)
    
    def generate_structured_output(self, prompt: str, schema: Dict[str, Any]) -> GeminiResponse:
        """
        Generate structured output using Gemini API with JSON schema.
        
        Args:
            prompt: Input prompt
            schema: JSON schema for structured output
            
        Returns:
            GeminiResponse object
        """
        # Add schema instruction to prompt
        structured_prompt = f"""{prompt}

Please respond with valid JSON that matches this schema:
{json.dumps(schema, indent=2)}

Ensure your response is valid JSON only, no additional text."""
        
        payload = {
            "contents": [{
                "parts": [{"text": structured_prompt}]
            }],
            "generationConfig": {
                "temperature": 0.3,  # Lower temperature for structured output
                "maxOutputTokens": 2000,
                "topP": 0.8,
                "topK": 10
            }
        }
        
        endpoint = f"models/{self.model.value}:generateContent"
        return self._make_request(endpoint, payload)
    
    def health_check(self) -> bool:
        """
        Check if the Gemini API is accessible.
        
        Returns:
            True if API is accessible, False otherwise
        """
        try:
            # Simple test request
            response = self.generate_text("Hello", max_tokens=10)
            return response.success
        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")
            return False
