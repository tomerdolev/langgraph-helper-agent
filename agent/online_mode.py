import os
import requests

from .utils import call_gemini

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def tavily_search(query: str, max_results: int = 5) -> str:
    """
    Simple wrapper around Tavily search API (optional but nice).
    If no API key is set or an error occurs, returns an empty string.
    """
    if not TAVILY_API_KEY:
        return ""

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results,
        "search_depth": "basic",
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])

        combined = "\n\n---\n\n".join(
            f"Title: {r.get('title')}\nURL: {r.get('url')}\nContent: {r.get('content')}"
            for r in results
        )
        return combined
    except Exception:
        return ""


def answer_online(question: str) -> str:
    """
    Online mode:
    - Optionally uses Tavily web search (if TAVILY_API_KEY is set)
    - Uses Gemini with both its knowledge and the web results
    """

    web_context = tavily_search(
        f"LangGraph Python LangChain Python: {question}", max_results=5
    )

    system_instructions = (
        "You are an expert assistant for LangGraph and LangChain in Python.\n"
        "Use the web search context (if present) together with your own knowledge.\n"
        "Prioritize official LangGraph and LangChain concepts and best practices.\n"
        "Give clear, practical answers with Python code snippets when helpful."
    )

    if web_context:
        prompt = (
            f"{system_instructions}\n\n"
            f"### Web search context\n{web_context}\n\n"
            f"### Question\n{question}\n\n"
            "### Answer:"
        )
    else:
        prompt = (
            f"{system_instructions}\n\n"
            f"Question: {question}\n\n"
            "Answer:"
        )

    return call_gemini(prompt)
