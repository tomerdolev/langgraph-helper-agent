import os
from pathlib import Path
from .utils import call_gemini

# Determine absolute project root
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# Create folder if missing
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def load_offline_docs():
    """
    Load all .txt files from data/ directory.
    Returns concatenated string of all documentation.
    """
    docs = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            path = os.path.join(DATA_DIR, filename)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                docs.append(f.read())
    
    if not docs:
        return "No offline documentation found. Run scripts/download_docs.py first."
    
    return "\n\n".join(docs)


def answer_offline(query: str) -> str:
    """
    Answer query using only offline documentation.
    No web access used (only local files + Gemini API).
    """
    docs = load_offline_docs()
    
    # Limit docs to avoid token limits (adjust as needed)
    max_chars = 30000
    if len(docs) > max_chars:
        docs = docs[:max_chars] + "\n\n[Documentation truncated...]"
    
    prompt = f"""You are a helpful assistant for LangGraph and LangChain documentation.

OFFLINE MODE: Answer using ONLY the documentation provided below.

User Question:
{query}

Offline Documentation:
{docs}

Instructions:
- Answer based ONLY on the documentation above
- Be specific and cite relevant parts
- If the answer is not in the docs, say so clearly
- Provide code examples when available in the docs

Answer:"""
    
    return call_gemini(prompt)