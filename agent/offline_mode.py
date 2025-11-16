import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import GenerativeModel

# Load .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Determine absolute project root:
# This file is located in: langgraph-helper-agent/agent/
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)  # go up 1 level
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# Create folder if missing
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def load_offline_docs():
    docs = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            path = os.path.join(DATA_DIR, filename)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                docs.append(f.read())
    return "\n\n".join(docs)


def answer_offline(query: str) -> str:
    docs = load_offline_docs()

    model = GenerativeModel("models/gemini-2.5-flash")

    prompt = f"""
Offline mode:

User question:
{query}

Offline documentation:
{docs[:7000]}

Answer ONLY using the documentation above.
"""

    response = model.generate_content(prompt)
    return response.text if response else "No response from Gemini."
