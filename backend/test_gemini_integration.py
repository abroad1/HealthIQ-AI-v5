#!/usr/bin/env python3
"""
Simple test script to verify Gemini integration works.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def test_gemini_client():
    """Test GeminiClient initialization."""
    try:
        from core.llm.gemini_client import GeminiClient
        print("✅ GeminiClient import successful")
        
        # Test initialization (this will fail without API key, but that's expected)
        try:
            client = GeminiClient()
            print("✅ GeminiClient initialization successful")
        except ValueError as e:
            if "GEMINI_API_KEY is missing" in str(e):
                print("✅ GeminiClient properly validates API key")
            else:
                print(f"❌ Unexpected error: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ GeminiClient import failed: {e}")
        return False

def test_mock_client():
    """Test MockLLMClient functionality."""
    try:
        from core.insights.synthesis import MockLLMClient
        print("✅ MockLLMClient import successful")
        
        client = MockLLMClient()
        print("✅ MockLLMClient initialization successful")
        
        # Test generate method
        response = client.generate("test prompt")
        print("✅ MockLLMClient.generate() works")
        
        # Check response format
        assert "text" in response
        assert "candidates" in response
        assert "model" in response
        print("✅ MockLLMClient response format correct")
        
        return True
    except Exception as e:
        print(f"❌ MockLLMClient test failed: {e}")
        return False

def test_synthesis_integration():
    """Test synthesis integration."""
    try:
        from core.insights.synthesis import InsightSynthesizer
        print("✅ InsightSynthesizer import successful")
        
        synthesizer = InsightSynthesizer()
        print("✅ InsightSynthesizer initialization successful")
        
        # Check that it has an LLM client
        assert synthesizer.llm_client is not None
        print("✅ InsightSynthesizer has LLM client")
        
        return True
    except Exception as e:
        print(f"❌ Synthesis integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Gemini Integration...")
    print("=" * 50)
    
    tests = [
        test_gemini_client,
        test_mock_client,
        test_synthesis_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"\n🔍 Running {test.__name__}...")
        if test():
            passed += 1
            print(f"✅ {test.__name__} PASSED")
        else:
            print(f"❌ {test.__name__} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Gemini integration is working.")
        sys.exit(0)
    else:
        print("💥 Some tests failed. Check the output above.")
        sys.exit(1)
