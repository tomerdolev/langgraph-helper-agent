import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Load API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in your .env file")

# Configure Gemini client
genai.configure(api_key=GEMINI_API_KEY)

def call_gemini(prompt: str) -> str:
    """
    Calls Gemini API with a simple text prompt.
    Returns the response text.
    """

    # Use the NEW, VALID MODEL
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)
    return response.text if response else "No response from Gemini."
