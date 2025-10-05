import google.generativeai as genai
from config.ai import LLMConfig
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import time
import random

class LLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def generate_insights(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        category: str
    ) -> Dict[str, Any]:
        """
        Generate insights using LLM.
        
        Args:
            system_prompt: System prompt for the LLM
            user_prompt: User prompt with data
            category: Health category
            
        Returns:
            LLM response with insights
        """
        pass

class GeminiClient(LLMClient):
    """
    Production Gemini LLM client.
    Uses google-generativeai SDK and enforces HealthIQ AI policy.
    """

    def __init__(self, model: str | None = None):
        # Default to stable, supported model
        self.model_name = model or "models/gemini-flash-latest"

        # Configure SDK
        api_key = LLMConfig.API_KEYS.get("gemini")
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY is missing in .env")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.model_name)
    def generate(self, prompt: str, input_files: Optional[List[tuple]] = None, **kwargs) -> dict:
        """
        Generate content from Gemini with retry logic and error handling.
        Supports both text prompts and multimodal input with files.
        
        Args:
            prompt: Text prompt for the LLM
            input_files: List of (mime_type, file_bytes) tuples for multimodal input
            **kwargs: Additional arguments for generate_content
            
        Returns:
            Structured dict with text and metadata
        """
        max_retries = 3
        base_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                
                # Prepare content for multimodal input
                if input_files:
                    content_parts = [prompt]
                    for mime_type, file_bytes in input_files:
                        content_parts.append({
                            "mime_type": mime_type,
                            "data": file_bytes
                        })
                    response = self.model.generate_content(content_parts, **kwargs)
                else:
                    response = self.model.generate_content(prompt, **kwargs)
                
                latency_ms = int((time.time() - start_time) * 1000)
                
                # Extract token count safely
                tokens_used = 0
                if hasattr(response, "usage_metadata") and response.usage_metadata:
                    tokens_used = getattr(response.usage_metadata, "total_token_count", 0)
                
                return {
                    "text": response.text,
                    "candidates": [c.text for c in getattr(response, "candidates", []) if hasattr(c, "text")],
                    "model": self.model_name,
                    "tokens_used": tokens_used,
                    "latency_ms": latency_ms,
                }
            except Exception as e:
                if attempt == max_retries - 1:
                    # Final attempt failed, return error
                    return {
                        "text": None,
                        "error": str(e),
                        "model": self.model_name,
                        "tokens_used": 0,
                        "latency_ms": 0,
                    }
                else:
                    # Exponential backoff with jitter
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(delay)
        
        # Should never reach here, but just in case
        return {
            "text": None,
            "error": "Max retries exceeded",
            "model": self.model_name,
            "tokens_used": 0,
            "latency_ms": 0,
        }
    
    def generate_insights(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        category: str
    ) -> Dict[str, Any]:
        """
        Generate insights using Gemini (implements LLMClient interface).
        
        Args:
            system_prompt: System prompt for the LLM
            user_prompt: User prompt with data
            category: Health category
            
        Returns:
            Gemini response with insights
        """
        # Combine system and user prompts
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        return self.generate(full_prompt)
