"""
Unit tests for GeminiClient - safe tests that mock API calls.
"""

import pytest
from unittest.mock import patch, MagicMock
from core.llm.gemini_client import GeminiClient


class TestGeminiClient:
    """Test GeminiClient with mocked API calls."""
    
    @patch('core.llm.gemini_client.genai')
    @patch('core.llm.gemini_client.LLMConfig')
    def test_initialization_with_default_model(self, mock_config, mock_genai):
        """Test GeminiClient initializes with default model."""
        # Setup mock
        mock_config.API_KEYS = {"gemini": "test-api-key"}
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Test initialization
        client = GeminiClient()
        
        # Verify configuration
        assert client.model_name == "models/gemini-flash-latest"
        mock_genai.configure.assert_called_once_with(api_key="test-api-key")
        mock_genai.GenerativeModel.assert_called_once_with("models/gemini-flash-latest")
    
    @patch('core.llm.gemini_client.genai')
    @patch('core.llm.gemini_client.LLMConfig')
    def test_initialization_with_custom_model(self, mock_config, mock_genai):
        """Test GeminiClient initializes with custom model."""
        # Setup mock
        mock_config.API_KEYS = {"gemini": "test-api-key"}
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Test initialization with custom model
        client = GeminiClient(model="models/gemini-pro")
        
        # Verify configuration
        assert client.model_name == "models/gemini-pro"
        mock_genai.GenerativeModel.assert_called_once_with("models/gemini-pro")
    
    @patch('core.llm.gemini_client.genai')
    @patch('core.llm.gemini_client.LLMConfig')
    def test_initialization_missing_api_key(self, mock_config, mock_genai):
        """Test GeminiClient raises error when API key is missing."""
        # Setup mock with missing API key
        mock_config.API_KEYS = {"gemini": None}
        
        # Test that initialization raises ValueError
        with pytest.raises(ValueError, match="❌ GEMINI_API_KEY is missing in .env"):
            GeminiClient()
    
    @patch('core.llm.gemini_client.genai')
    @patch('core.llm.gemini_client.LLMConfig')
    def test_generate_success(self, mock_config, mock_genai):
        """Test successful content generation."""
        # Setup mocks
        mock_config.API_KEYS = {"gemini": "test-api-key"}
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Mock successful response with usage metadata
        mock_response = MagicMock()
        mock_response.text = "Test response from Gemini"
        mock_response.candidates = [MagicMock(text="candidate 1"), MagicMock(text="candidate 2")]
        mock_usage_metadata = MagicMock()
        mock_usage_metadata.total_token_count = 150
        mock_response.usage_metadata = mock_usage_metadata
        mock_model.generate_content.return_value = mock_response
        
        # Test generation
        client = GeminiClient()
        result = client.generate("Test prompt")
        
        # Verify result
        assert result["text"] == "Test response from Gemini"
        assert result["candidates"] == ["candidate 1", "candidate 2"]
        assert result["model"] == "models/gemini-flash-latest"
        assert result["tokens_used"] == 150
        assert result["latency_ms"] >= 0
        assert "error" not in result
        
        # Verify API call
        mock_model.generate_content.assert_called_once_with("Test prompt")
    
    @patch('core.llm.gemini_client.genai')
    @patch('core.llm.gemini_client.LLMConfig')
    def test_generate_insights_interface(self, mock_config, mock_genai):
        """Test generate_insights method implements LLMClient interface."""
        # Setup mocks
        mock_config.API_KEYS = {"gemini": "test-api-key"}
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Mock successful response
        mock_response = MagicMock()
        mock_response.text = "Test insights response"
        mock_response.candidates = []
        mock_usage_metadata = MagicMock()
        mock_usage_metadata.total_token_count = 100
        mock_response.usage_metadata = mock_usage_metadata
        mock_model.generate_content.return_value = mock_response
        
        # Test generate_insights method
        client = GeminiClient()
        result = client.generate_insights(
            system_prompt="System prompt",
            user_prompt="User prompt",
            category="metabolic"
        )
        
        # Verify result
        assert result["text"] == "Test insights response"
        assert result["model"] == "models/gemini-flash-latest"
        assert result["tokens_used"] == 100
        assert result["latency_ms"] >= 0
        
        # Verify API call with combined prompt
        mock_model.generate_content.assert_called_once_with("System prompt\n\nUser prompt")
    
    @patch('core.llm.gemini_client.genai')
    @patch('core.llm.gemini_client.LLMConfig')
    def test_generate_with_kwargs(self, mock_config, mock_genai):
        """Test content generation with additional parameters."""
        # Setup mocks
        mock_config.API_KEYS = {"gemini": "test-api-key"}
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Mock successful response
        mock_response = MagicMock()
        mock_response.text = "Test response"
        mock_response.candidates = []
        mock_model.generate_content.return_value = mock_response
        
        # Test generation with kwargs
        client = GeminiClient()
        result = client.generate("Test prompt", temperature=0.7, max_tokens=100)
        
        # Verify API call with kwargs
        mock_model.generate_content.assert_called_once_with("Test prompt", temperature=0.7, max_tokens=100)
    
    @patch('core.llm.gemini_client.genai')
    @patch('core.llm.gemini_client.LLMConfig')
    def test_generate_api_error(self, mock_config, mock_genai):
        """Test graceful handling of API errors."""
        # Setup mocks
        mock_config.API_KEYS = {"gemini": "test-api-key"}
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Mock API error
        mock_model.generate_content.side_effect = Exception("API Error")
        
        # Test generation with error
        client = GeminiClient()
        result = client.generate("Test prompt")
        
        # Verify error handling
        assert result["text"] is None
        assert result["error"] == "API Error"
        assert result["model"] == "models/gemini-flash-latest"
        assert result["tokens_used"] == 0
        assert result["latency_ms"] == 0
    
    @patch('core.llm.gemini_client.genai')
    @patch('core.llm.gemini_client.LLMConfig')
    @patch('core.llm.gemini_client.time.sleep')  # Mock sleep to speed up test
    def test_generate_retry_logic(self, mock_sleep, mock_config, mock_genai):
        """Test retry logic with exponential backoff."""
        # Setup mocks
        mock_config.API_KEYS = {"gemini": "test-api-key"}
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Mock first two calls fail, third succeeds
        mock_response = MagicMock()
        mock_response.text = "Success after retries"
        mock_response.candidates = []
        mock_usage_metadata = MagicMock()
        mock_usage_metadata.total_token_count = 50
        mock_response.usage_metadata = mock_usage_metadata
        
        mock_model.generate_content.side_effect = [
            Exception("Temporary error 1"),
            Exception("Temporary error 2"),
            mock_response
        ]
        
        # Test generation with retries
        client = GeminiClient()
        result = client.generate("Test prompt")
        
        # Verify success after retries
        assert result["text"] == "Success after retries"
        assert result["tokens_used"] == 50
        assert result["latency_ms"] >= 0
        assert "error" not in result
        
        # Verify retry attempts
        assert mock_model.generate_content.call_count == 3
        assert mock_sleep.call_count == 2  # Two retries, two sleeps
    
    @patch('core.llm.gemini_client.genai')
    @patch('core.llm.gemini_client.LLMConfig')
    def test_generate_no_candidates(self, mock_config, mock_genai):
        """Test handling of response with no candidates."""
        # Setup mocks
        mock_config.API_KEYS = {"gemini": "test-api-key"}
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Mock response with no candidates
        mock_response = MagicMock()
        mock_response.text = "Test response"
        mock_response.candidates = []
        mock_model.generate_content.return_value = mock_response
        
        # Test generation
        client = GeminiClient()
        result = client.generate("Test prompt")
        
        # Verify result
        assert result["text"] == "Test response"
        assert result["candidates"] == []
        assert result["model"] == "models/gemini-flash-latest"
    
    @patch('core.llm.gemini_client.genai')
    @patch('core.llm.gemini_client.LLMConfig')
    def test_generate_candidates_without_text(self, mock_config, mock_genai):
        """Test handling of candidates without text attribute."""
        # Setup mocks
        mock_config.API_KEYS = {"gemini": "test-api-key"}
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Mock response with candidates without text
        mock_response = MagicMock()
        mock_response.text = "Test response"
        mock_candidate = MagicMock()
        del mock_candidate.text  # Remove text attribute
        mock_response.candidates = [mock_candidate]
        mock_model.generate_content.return_value = mock_response
        
        # Test generation
        client = GeminiClient()
        result = client.generate("Test prompt")
        
        # Verify result (candidates without text should be filtered out)
        assert result["text"] == "Test response"
        assert result["candidates"] == []
        assert result["model"] == "models/gemini-flash-latest"
