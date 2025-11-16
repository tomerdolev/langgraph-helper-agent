<!-- Copilot instructions for the langgraph-helper-agent repo -->
# Project Orientation for AI Coding Agents

This repository implements a tiny helper agent with two operation modes: an
offline documentation retriever and an online LLM caller. The goal of these
instructions is to help AI coding assistants become productive quickly by
pointing to the project's architecture, conventions, and important files.

Key files/locations
- `main.py` — simple CLI entrypoint. Use `--mode online|offline` and a single
  query string. Example: `python .\main.py --mode offline "list llms"`.
- `agent/` — core package. Exports `answer_offline` and `answer_online` from
  `agent/__init__.py` (see that file when adding new public functions).
- `agent/offline_mode.py` — naive offline search that concatenates files from
  `agent/data/` and returns documentation on match.
- `agent/retrieval.py` — `OfflineRetriever` uses `TfidfVectorizer` +
  `cosine_similarity` to find top-k document matches. Use this as the
  canonical example when adding more advanced retrieval logic.
- `agent/utils.py` — Gemini API wiring. Loads `GEMINI_API_KEY` from `.env` and
  configures `google.generativeai`.
- `scripts/download_docs.py` — populates `agent/data/` with `.txt` lists used
  for offline mode (calls remote URLs listed in the script).

Essential architecture / data flow
- CLI (`main.py`) → `agent` package. The `agent` package exposes two simple
  functions: `answer_offline(query: str)` and `answer_online(query: str)`.
- Offline mode: `scripts/download_docs.py` downloads `.txt` files into
  `agent/data/`. `OfflineRetriever` or `offline_mode.load_offline_docs()` read
  these files and search locally.
- Online mode: `agent.online_mode.answer_online` calls `agent.utils.call_gemini`
  which uses `google.generativeai` and the `GEMINI_API_KEY` environment var.

Project-specific conventions and patterns
- Minimal public surface: new features intended for the CLI should expose a
  single function and be re-exported in `agent/__init__.py`.
- Data files are plain text `.txt` under `agent/data/`. Retrieval functions
  expect `.txt` documents; follow that format for new offline resources.
- The repo prefers small, focused modules: keep LLM wiring in `utils.py`,
  retrieval code in `retrieval.py`, and CLI glue in `main.py`.
- Environment variables are loaded with `python-dotenv` in `utils.py`. Do not
  hardcode API keys — use `.env` or process environment variables.

Developer workflows and commands (Windows PowerShell)
- Create and activate a virtualenv (PowerShell):
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- Install dependencies:
  ```powershell
  pip install -r requirements.txt
  ```
- Populate offline docs (required for offline mode):
  ```powershell
  python .\scripts\download_docs.py
  ```
- Run CLI examples:
  ```powershell
  python .\main.py --mode offline "what llms are supported"
  python .\main.py --mode online "summarize the project"
  ```

Important integration points & gotchas
- `agent/utils.py` raises `ValueError` when `GEMINI_API_KEY` is missing. If
  you see that error, add a `.env` with `GEMINI_API_KEY=...` or export the
  environment variable before running online mode.
- The default model used is `gemini-1.5-flash` (see `utils.py`). Updates to
  model names should be made in `call_gemini` and `.env.example` if needed.
- Offline retrieval uses scikit-learn TF-IDF vectors. If adding large
  documents or many files, consider batching or caching vectorizer state to
  avoid expensive re-fits on every startup.

When editing code
- Follow the existing split: API wiring in `utils.py`, retrieval in
  `retrieval.py`, CLI glue in `main.py`. Re-export public API from
  `agent/__init__.py`.
- Reference examples when implementing features:
  - Use `OfflineRetriever.search(query, top_k=3)` as the template for
    vector-search behavior.
  - Use `scripts/download_docs.py` for URL additions and `agent/data/` writes.

Where to look for more context
- `agent/` modules for concrete code examples.
- `scripts/download_docs.py` for the exact URLs and download flow.
- `.env.example` (contains `GEMINI_API_KEY` and `GEMINI_MODEL`) — do not
  commit real keys.

If anything above is unclear or you want more depth (unit tests, CI,
or a sample `.env` management flow), tell me which area to expand or clarify.
