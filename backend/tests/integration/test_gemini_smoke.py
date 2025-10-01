import os
import pytest
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv(find_dotenv(), override=True)

# Skip this test in CI/CD to avoid burning quota
skip_in_ci = os.getenv("CI", "").lower() == "true"

@pytest.mark.skipif(skip_in_ci, reason="Skipped in CI/CD to avoid Gemini API usage")
@pytest.mark.integration
def test_gemini_smoke():
    api_key = os.getenv("GEMINI_API_KEY")
    assert api_key, "❌ GEMINI_API_KEY must be set in .env for smoke test"

    genai.configure(api_key=api_key)

    # Use a stable, available model
    model = genai.GenerativeModel("models/gemini-flash-latest")

    response = model.generate_content("Hello from HealthIQ AI v5. Respond with a short confirmation.")

    assert response and response.text, "❌ No response from Gemini API"
    print("\n✅ Gemini responded:", response.text)
