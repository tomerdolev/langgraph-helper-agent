# LangGraph Helper Agent

A compact helper agent that demonstrates two main capabilities:

- Offline documentation retrieval (local `.txt` resources under `data/`).
- Online LLM-backed responses (via the Google Gemini client wrapper in
  `agent/utils.py`).

This README documents the complete codebase: CLI, agent package, retrieval
implementation, LLM wiring, helper scripts, and environment expectations.

## Repository layout (important files)

- `main.py` — CLI entrypoint. Usage: `python .\main.py --mode <online|offline> "<query>"`.
- `agent/__init__.py` — public exports: `answer_offline`, `answer_online`.
- `agent/offline_mode.py` — helper functions for reading `data/` and
  a very small `answer_offline(query: str) -> str` fallback.
- `agent/retrieval.py` — `OfflineRetriever` class showing TF-IDF +
  `cosine_similarity` based search.
- `agent/online_mode.py` — thin wrapper that calls `agent.utils.call_gemini`.
- `agent/utils.py` — loads `.env`, configures `google.generativeai`, and
  defines `call_gemini(prompt: str) -> str`.
- `data/` — directory containing `.txt` documents used by offline mode.
- `scripts/download_docs.py` — downloads example `.txt` docs into
  `data/` (contains canonical source URLs used by the project).
- `.env.example` — shows required environment variables (`GEMINI_API_KEY`).
- `requirements.txt` — runtime dependencies (`python-dotenv`, `requests`,
  `scikit-learn`, `numpy`, `scipy`).

## High-level architecture and data flow

1. User runs CLI (`main.py`) with `--mode` and a query.
2. If `offline`, the CLI calls `answer_offline(query)` which uses either
   `offline_mode.load_offline_docs()` (simple concatenation + substring
   search) or can be replaced with `OfflineRetriever` from
   `agent/retrieval.py` for TF-IDF ranking (reads from `data/`).
3. If `online`, the CLI calls `answer_online(query)` which delegates to
   `agent.utils.call_gemini(prompt)` to call the Gemini API and return text.

This separation keeps retrieval and LLM code separate and easy to replace.

## Online Mode (Required)

The online mode enables the agent to fetch up-to-date information from the web.
This project uses only free-tier or free-to-use services.

Search Provider
- DuckDuckGo Instant Answer API (`https://api.duckduckgo.com/?q=<query>&format=json`) — free, no API key required.

How online mode works
1. The agent sends the user query to DuckDuckGo Search (Instant Answer API).
2. The search JSON results are parsed and cleaned (abstract, related topics, and result snippets).
3. Relevant text snippets are combined into a contextual prompt for the LLM.
4. The prompt is passed to Gemini for synthesis (see `agent/utils.py`).
5. The final answer merges online findings with LLM reasoning and is returned to the user.

Why DuckDuckGo
- 100% free
- No authentication required
- No API key or usage limits for basic search
- Suitable for developer documentation lookups and portable across machines

Note: Users must only provide a Gemini API key via `.env`. No additional API keys are required for online mode.

## Offline Mode (Required)

The offline mode allows the agent to operate without internet access (except
for the Gemini API, which is permitted by the assignment). It uses only the
local `.txt` documentation files located under `data/`.

How offline mode works:
1. The agent loads all `.txt` files from `data/`.
2. The files represent the LangGraph and LangChain documentation in `llms.txt` format.
3. A simple substring search or TF-IDF ranking (via `OfflineRetriever`) is applied.
4. The retrieved text is returned directly to the user without using any online resources.
5. If no match is found, a fallback message is returned.

Data sources used in offline mode:
- `https://langchain-ai.github.io/langgraph/llms.txt`
- `https://langchain-ai.github.io/langgraph/llms-full.txt`
- `https://python.langchain.com/llms.txt`

Offline mode fully satisfies the assignment requirement for operating with
pre-downloaded documentation and no internet access.

## Detailed component notes

agent/offline_mode.py
- `DATA_DIR` is `data/` relative to the project root.
- `load_offline_docs()` reads all `.txt` files and returns a single
  concatenated string. It is used by `answer_offline(query)` which performs
  a case-insensitive substring search. If any match exists, the full docs
  text is returned with a header; otherwise a fallback message is returned.

agent/retrieval.py
- `OfflineRetriever(data_path: Path)` loads all `.txt` files, fits a
  `TfidfVectorizer`, and exposes `search(query: str, top_k=3)` returning the
  top-k matching document strings. Use this class when you need ranked
  results instead of the substring fallback.

agent/utils.py
- Loads `.env` using `python-dotenv` and reads `GEMINI_API_KEY`.
- Raises `ValueError` if `GEMINI_API_KEY` is not present — online mode
  cannot function without it.
- Configures `google.generativeai` and constructs a model with
  `genai.GenerativeModel("gemini-1.5-flash")`, then calls
  `model.generate_content(prompt)` and returns `response.text`.

scripts/download_docs.py
- Defines `URLS` mapping file names to remote `.txt` resources. Running
  this script downloads each and writes into `data/`. It's the
  canonical way to populate offline docs for testing.

.env.example
- Contains example keys and the `GEMINI_MODEL` placeholder. Replace with
  your environment-secret values in a local `.env` file. Do NOT commit real
  keys to source control.

## Quick start (Windows PowerShell)

1. Create and activate virtual environment, then install deps:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. (Optional) Populate offline docs for offline testing:

```powershell
python .\scripts\download_docs.py
```

This will download the latest `.txt` files into the `data/` directory.

3. Run the CLI in offline mode:

```powershell
python .\main.py --mode offline "what llms are supported"
```

4. Run the CLI in online mode (requires `.env` with `GEMINI_API_KEY`):

```powershell
python .\main.py --mode online "summarize the project"
```

You can also set the mode via environment variable and omit `--mode`:

```powershell
$env:AGENT_MODE = "online"
python .\main.py "summarize the project"
```

## Testing and quick checks

- Manual smoke tests: run the CLI with sample queries as above.
- Suggested unit test to add (example): test that `OfflineRetriever.search`
  returns expected number of items and that `offline_mode.load_offline_docs()`
  loads files from `data/`.

Example pytest (not included):

```python
def test_retriever(tmp_path):
    # create sample files in tmp_path
    # instantiate OfflineRetriever(tmp_path) and assert search results
    pass
```

## Data Freshness Strategy

This project supports both static (offline) and dynamic (online) data sources.

Offline Data
- The `.txt` files inside `data/` may become outdated. Users can refresh
  the offline knowledge base manually by re-downloading the latest `.txt`
  documents from the official sources (these are the same URLs used by
  `scripts/download_docs.py`):

  - LangGraph Docs:
    - `https://langchain-ai.github.io/langgraph/llms.txt`
    - `https://langchain-ai.github.io/langgraph/llms-full.txt`

  - LangChain Python Docs:
    - `https://python.langchain.com/llms.txt`

- Run `python .\scripts\download_docs.py` to automatically refresh the
  `data/` directory with the latest `.txt` files. This is the canonical
  data preparation and refresh workflow for offline mode.

Online Data
- Online mode uses live DuckDuckGo search results for every query. Because
  no caching is performed, online mode always fetches fresh data and does
  not require manual offline refreshes.

This dual approach satisfies the assignment requirement of supporting both
local static data and remote dynamic data.

## Assignment mapping: AI Technical Assignment - LangGraph Helper Agent

This repository is organized to satisfy the assignment requirements. Summary:

- Dual Operating Modes: Supported via `--mode` CLI flag or `AGENT_MODE` env var.
  - Offline Mode: works without web access, uses local `data/*.txt` (see
    `scripts/download_docs.py` for data preparation).
  - Online Mode: uses DuckDuckGo Instant Answer API (free) + Gemini (LLM).
- Language Model: Gemini is used via `google.generativeai`.
  - Obtain a Gemini API key from Google AI Studio: `https://studio.research.google.com/`.
- Technical Stack: Python; minimal, portable implementation. Dependencies in
  `requirements.txt`.
- Documentation Sources: The repository uses the provided `llms.txt` sources
  and `scripts/download_docs.py` automates retrieval. Additional sources may
  be added and must be documented in the README and refresh workflow.
- Portability: Clear setup, dependency management, and environment guidance
  are included in this README.

## Example questions the agent should handle

- "How do I add persistence to a LangGraph agent?"
- "What's the difference between StateGraph and MessageGraph?"
- "Show me how to implement human-in-the-loop with LangGraph"
- "How do I handle errors and retries in LangGraph nodes?"
- "What are best practices for state management in LangGraph?"

These are example prompts the agent aims to support using the offline docs
and online search + Gemini pipeline.

## Extending the project

- Add new CLI features by providing a single function in `agent/` and
  re-exporting it from `agent/__init__.py` so `main.py` can call it.
- To swap LLM providers, modify `agent/utils.py` but keep a single function
  `call_gemini(prompt: str) -> str` (or rename consistently) so the
  `answer_online` wrapper stays thin.
- To improve offline retrieval at scale, persist the TF-IDF/vectorizer
  state or switch to an embeddings-based index. The `OfflineRetriever` is
  the implementation to build on.

## Security & privacy

- Do not commit `.env` with real keys. Use `.env` locally and keep secrets
  out of source control.
- The `scripts/download_docs.py` fetches remote content; review sources if
  you need to control provenance of the offline docs.

## Contributing

1. Open an issue describing desired change or bug.
2. Implement a focused change and push a PR. Keep modules small and tests
   scoped to the change.

## License

This repository does not include a license file. Add a `LICENSE` to clarify
terms for contributors and users.

