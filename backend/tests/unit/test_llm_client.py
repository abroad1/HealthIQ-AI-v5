"""
Unit tests for Gemini LLM client.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json

from core.llm.client import GeminiClient, GeminiModel, GeminiResponse, GeminiError, GeminiRateLimitError, GeminiAPIError
from config.env import settings


class TestGeminiClient:
    """Test cases for GeminiClient."""
    
    def test_init_with_api_key(self):
        """Test client initialization with API key."""
        client = GeminiClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.model == GeminiModel.GEMINI_PRO
    
    def test_init_without_api_key(self):
        """Test client initialization without API key."""
        with patch.object(settings, 'GEMINI_API_KEY', 'env_key'):
            client = GeminiClient()
            assert client.api_key == "env_key"
    
    def test_init_without_api_key_raises_error(self):
        """Test client initialization without API key raises error."""
        with patch.object(settings, 'GEMINI_API_KEY', None):
            with pytest.raises(ValueError, match="GEMINI_API_KEY not found"):
                GeminiClient()
    
    def test_init_with_custom_model(self):
        """Test client initialization with custom model."""
        client = GeminiClient(api_key="test_key", model=GeminiModel.GEMINI_FLASH)
        assert client.model == GeminiModel.GEMINI_FLASH
    
    @patch('core.llm.client.requests.Session.post')
    def test_generate_text_success(self, mock_post):
        """Test successful text generation."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{"text": "Generated text response"}]
                }
            }],
            "usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 5}
        }
        mock_post.return_value = mock_response
        
        client = GeminiClient(api_key="test_key")
        response = client.generate_text("Test prompt")
        
        assert response.success is True
        assert response.content == "Generated text response"
        assert response.model == GeminiModel.GEMINI_PRO.value
    
    @patch('core.llm.client.requests.Session.post')
    def test_generate_text_rate_limit_error(self, mock_post):
        """Test rate limit error handling."""
        # Mock rate limit response
        mock_response = Mock()
        mock_response.status_code = 429
        mock_post.return_value = mock_response
        
        client = GeminiClient(api_key="test_key")
        
        with pytest.raises(GeminiRateLimitError):
            client.generate_text("Test prompt")
    
    @patch('core.llm.client.requests.Session.post')
    def test_generate_text_api_error(self, mock_post):
        """Test API error handling."""
        # Mock API error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.ok = False
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response
        
        client = GeminiClient(api_key="test_key")
        
        with pytest.raises(GeminiAPIError):
            client.generate_text("Test prompt")
    
    @patch('core.llm.client.requests.Session.post')
    def test_generate_text_timeout(self, mock_post):
        """Test timeout error handling."""
        # Mock timeout
        from requests.exceptions import Timeout
        mock_post.side_effect = Timeout("Request timeout")
        
        client = GeminiClient(api_key="test_key")
        response = client.generate_text("Test prompt")
        
        assert response.success is False
        assert "timeout" in response.error.lower()
    
    @patch('core.llm.client.requests.Session.post')
    def test_generate_structured_output_success(self, mock_post):
        """Test successful structured output generation."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{"text": '{"result": "success"}'}]
                }
            }],
            "usageMetadata": {"promptTokenCount": 20, "candidatesTokenCount": 10}
        }
        mock_post.return_value = mock_response
        
        client = GeminiClient(api_key="test_key")
        schema = {"type": "object", "properties": {"result": {"type": "string"}}}
        response = client.generate_structured_output("Test prompt", schema)
        
        assert response.success is True
        assert response.content == '{"result": "success"}'
    
    @patch('core.llm.client.requests.Session.post')
    def test_health_check_success(self, mock_post):
        """Test successful health check."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{"text": "Hello"}]
                }
            }],
            "usageMetadata": {"promptTokenCount": 1, "candidatesTokenCount": 1}
        }
        mock_post.return_value = mock_response
        
        client = GeminiClient(api_key="test_key")
        result = client.health_check()
        
        assert result is True
    
    @patch('core.llm.client.requests.Session.post')
    def test_health_check_failure(self, mock_post):
        """Test failed health check."""
        # Mock failed response
        mock_post.side_effect = Exception("Connection error")
        
        client = GeminiClient(api_key="test_key")
        result = client.health_check()
        
        assert result is False
    
    def test_make_request_payload_structure(self):
        """Test that request payload has correct structure."""
        client = GeminiClient(api_key="test_key")
        
        # Test generate_text payload
        with patch.object(client, '_make_request') as mock_make_request:
            client.generate_text("Test prompt", max_tokens=500, temperature=0.5)
            
            # Verify _make_request was called
            assert mock_make_request.called
            
            # Get the call arguments
            call_args = mock_make_request.call_args
            endpoint = call_args[0][0]
            payload = call_args[0][1]
            
            # Verify endpoint
            assert endpoint == f"models/{GeminiModel.GEMINI_PRO.value}:generateContent"
            
            # Verify payload structure
            assert "contents" in payload
            assert "generationConfig" in payload
            assert payload["generationConfig"]["temperature"] == 0.5
            assert payload["generationConfig"]["maxOutputTokens"] == 500
    
    def test_make_request_structured_output_payload(self):
        """Test that structured output request payload has correct structure."""
        client = GeminiClient(api_key="test_key")
        
        # Test generate_structured_output payload
        with patch.object(client, '_make_request') as mock_make_request:
            schema = {"type": "object"}
            client.generate_structured_output("Test prompt", schema)
            
            # Verify _make_request was called
            assert mock_make_request.called
            
            # Get the call arguments
            call_args = mock_make_request.call_args
            endpoint = call_args[0][0]
            payload = call_args[0][1]
            
            # Verify endpoint
            assert endpoint == f"models/{GeminiModel.GEMINI_PRO.value}:generateContent"
            
            # Verify payload structure
            assert "contents" in payload
            assert "generationConfig" in payload
            assert payload["generationConfig"]["temperature"] == 0.3  # Lower for structured output
            
            # Verify prompt contains schema
            prompt = payload["contents"][0]["parts"][0]["text"]
            assert "JSON" in prompt
            assert "schema" in prompt.lower()
