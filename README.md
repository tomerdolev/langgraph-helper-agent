# LangGraph Helper Agent

An AI assistant that helps developers work with LangGraph and LangChain by answering practical questions. The agent supports both offline and online modes to handle different usage scenarios, such as working without internet access or integrating with live documentation sources.

## 🎯 Core Features

- **Dual Operating Modes**: Offline (local documentation) and Online (web search + LLM)
- **Smart Retrieval**: TF-IDF based document search for offline mode
- **LLM-Powered**: Uses Google Gemini for intelligent responses
- **Portable**: Easy setup with clear dependencies and environment configuration

---

## 📁 Repository Structure
```
langgraph-helper-agent/
├── agent/
│   ├── __init__.py          # Public exports
│   ├── offline_mode.py      # Offline mode implementation
│   ├── online_mode.py       # Online mode implementation
│   ├── retrieval.py         # TF-IDF document retriever
│   └── utils.py             # Gemini API configuration
├── data/                     # Offline documentation (.txt files)
├── scripts/
│   └── download_docs.py     # Download latest documentation
├── tests/
│   ├── __init__.py
│   └── test_offline.py      # Unit tests
├── .env                      # Your secrets (NOT committed)
├── .env.example             # Environment template (committed)
├── .gitignore               # Git ignore rules
├── main.py                  # CLI entrypoint
├── README.md                # This file
└── requirements.txt         # Python dependencies
```

---

## 🏗️ Architecture Overview

### High-Level Flow
```
User Query
    ↓
main.py (CLI)
    ↓
Mode Selection (--mode flag or AGENT_MODE env var)
    ↓
┌─────────────────┐         ┌─────────────────┐
│  Offline Mode   │         │   Online Mode   │
├─────────────────┤         ├─────────────────┤
│ 1. Load docs    │         │ 1. Web search   │
│    from data/   │         │    (Tavily API) │
│ 2. Search docs  │         │ 2. Combine with │
│    (substring   │         │    Gemini       │
│    or TF-IDF)   │         │ 3. Generate     │
│ 3. Pass to      │         │    answer       │
│    Gemini       │         │                 │
│ 4. Return       │         │                 │
└─────────────────┘         └─────────────────┘
         ↓                           ↓
    User receives answer
```

### Component Details

#### **main.py**
- CLI argument parsing
- Mode selection logic
- Delegates to `answer_offline()` or `answer_online()`

#### **agent/offline_mode.py**
- Loads all `.txt` files from `data/` directory
- Truncates to 30,000 characters to avoid token limits
- Passes documentation + query to Gemini
- Returns answer based solely on local docs

#### **agent/online_mode.py**
- Uses Tavily API for web search (optional)
- Searches for: "LangGraph Python LangChain Python: {query}"
- Combines search results with Gemini's knowledge
- Returns comprehensive answer with web context

#### **agent/retrieval.py**
- `OfflineRetriever` class using TF-IDF + cosine similarity
- Loads and indexes all `.txt` files
- Provides `search(query, top_k)` for ranked retrieval
- Can be used instead of simple substring search

#### **agent/utils.py**
- Centralized Gemini API configuration
- `call_gemini(prompt)` function used by both modes
- Handles API key validation

---

## 🚀 Quick Start

### 1. Clone and Setup Environment
```powershell
# Clone repository
git clone https://github.com/tomerdolev/langgraph-helper-agent.git
cd langgraph-helper-agent

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```powershell
# Copy example to create your .env file
copy .env.example .env
```

Edit `.env` and add your API key:
```bash
GEMINI_API_KEY=your_actual_key_here
```

**Get your Gemini API key:** https://aistudio.google.com/app/apikey

### 3. Download Offline Documentation (Optional)
```powershell
python .\scripts\download_docs.py
```

This downloads the latest documentation to `data/`:
- `langchain_llms.txt`
- `langgraph_llms.txt`
- `langgraph_llms_full.txt`

---

## 💻 Usage Examples

### Offline Mode
```powershell
python .\main.py --mode offline "How do I add persistence to a LangGraph agent?"
```

**Example Output:**
```
Based on the offline documentation, to add persistence to a LangGraph agent:

1. Use a Checkpointer: LangGraph provides checkpointers like MemorySaver 
   for in-memory persistence or SqliteSaver for database persistence.

2. Pass the checkpointer when compiling your graph:
   
   from langgraph.checkpoint.memory import MemorySaver
   
   checkpointer = MemorySaver()
   app = graph.compile(checkpointer=checkpointer)

3. Use thread_id when invoking to maintain conversation state:
   
   config = {"configurable": {"thread_id": "1"}}
   app.invoke({"messages": [...]}, config)

This allows your agent to remember previous interactions and resume from 
where it left off.
```

### Online Mode
```powershell
python .\main.py --mode online "What are the latest LangGraph features?"
```

**Example Output:**
```
Based on current web search results and documentation:

The latest LangGraph features include:

1. Streaming Support: Real-time streaming of agent actions and thoughts
2. Human-in-the-Loop: Built-in interrupts for human approval
3. Long-term Memory: Store and retrieve information across sessions
4. Multi-agent Systems: Coordinate multiple specialized agents
5. LangGraph Studio: Visual debugging and prototyping tool

These features make LangGraph ideal for building production-ready, 
stateful AI agents.
```

### Using Environment Variable
```powershell
# Set mode via environment variable
$env:AGENT_MODE = "offline"
python .\main.py "What's the difference between StateGraph and MessageGraph?"
```

---

## 📖 Operating Modes Explained

### Offline Mode

**How it works:**
1. Loads all `.txt` files from `data/` directory
2. Concatenates documentation (up to 30,000 characters)
3. Sends query + documentation to Gemini
4. Returns answer based **only** on local docs

**Data sources:**
- LangGraph: `https://langchain-ai.github.io/langgraph/llms.txt`
- LangGraph Full: `https://langchain-ai.github.io/langgraph/llms-full.txt`
- LangChain: `https://python.langchain.com/llms.txt`

**When to use:**
- ✅ No internet connection
- ✅ Want deterministic answers from known docs
- ✅ Privacy-sensitive environments

**Limitations:**
- ⚠️ Only knows information in downloaded docs
- ⚠️ Docs may become outdated

### Online Mode

**How it works:**
1. Searches web using Tavily API (optional) or falls back to Gemini's knowledge
2. Combines web results with query
3. Gemini synthesizes comprehensive answer
4. Returns answer with latest information

**External services used:**
- **Tavily Search API** (optional): Free tier, sign up at https://app.tavily.com/home
  - If no API key: Falls back to Gemini's built-in knowledge
- **Google Gemini**: Required, free tier available

**When to use:**
- ✅ Need latest information
- ✅ Query about recent features/updates
- ✅ Want comprehensive answers with web context

---

## 🔄 Data Freshness Strategy

### Offline Data Updates

**Manual update:**
```powershell
python .\scripts\download_docs.py
```

This fetches the latest documentation from official sources.

**Update frequency recommendation:**
- Monthly for active development
- Quarterly for stable usage

### Online Data

Online mode always fetches fresh data - no manual updates needed.

---

## 🧪 Testing

### Run Tests
```powershell
# Install pytest
pip install pytest

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=agent
```

### Test Coverage

Tests verify:
- ✅ Offline docs loading functionality
- ✅ OfflineRetriever search accuracy
- ✅ Top-k result limiting
- ✅ Empty query handling
- ✅ Edge cases

---

## 🎓 Example Questions

The agent can answer questions like:

- "How do I add persistence to a LangGraph agent?"
- "What's the difference between StateGraph and MessageGraph?"
- "Show me how to implement human-in-the-loop with LangGraph"
- "How do I handle errors and retries in LangGraph nodes?"
- "What are best practices for state management in LangGraph?"
- "How do I use checkpointers in LangGraph?"
- "What's new in the latest version of LangGraph?"

---

## 🛠️ Extending the Project

### Add New Agent Features

1. Create function in `agent/` module
2. Export from `agent/__init__.py`
3. Call from `main.py`

### Swap LLM Provider

Modify `agent/utils.py` to use different provider while keeping the same interface:
```python
def call_gemini(prompt: str) -> str:
    # Your custom LLM implementation here
    pass
```

### Improve Retrieval

The `OfflineRetriever` class can be extended:
- Add semantic embeddings (e.g., sentence-transformers)
- Implement caching for faster searches
- Add re-ranking algorithms

---

## 📋 Requirements

- **Python**: >= 3.10
- **Dependencies**: Listed in `requirements.txt` with versions
- **API Keys**: 
  - Google Gemini (required): https://aistudio.google.com/app/apikey
  - Tavily (optional): https://app.tavily.com/home

---

## 🔐 Security & Privacy

- ⚠️ **Never commit `.env`** - contains your API keys
- ✅ `.env` is in `.gitignore` to prevent accidental commits
- ✅ Use `.env.example` as template (no real keys)
- ⚠️ Review `scripts/download_docs.py` sources before running

---

## 🤝 Contributing

1. Open an issue describing the change or bug
2. Implement focused changes
3. Add tests for new functionality
4. Submit a pull request

---

## 📄 License

This repository does not currently include a license file. Consider adding an MIT or Apache 2.0 license for open contribution.

---

## 🎯 Assignment Compliance

This project fulfills all requirements of the AI Technical Assignment:

| Requirement | Status | Implementation |
|------------|--------|----------------|
| Dual Operating Modes | ✅ | `--mode` flag or `AGENT_MODE` env var |
| Offline Mode | ✅ | Uses local `data/*.txt` files |
| Online Mode | ✅ | Tavily API + Gemini |
| Google Gemini LLM | ✅ | Free tier via `google.generativeai` |
| Python Implementation | ✅ | Pure Python 3.10+ |
| Documentation Sources | ✅ | llms.txt format from official sources |
| Portability | ✅ | Clear setup, deps, env config |
| Mode Switching | ✅ | CLI flag and environment variable |
| Free Tier Services | ✅ | All services have free tiers |
| Data Freshness | ✅ | Manual offline updates, auto online |

---

## 📞 Support

For questions or issues:
1. Check existing GitHub issues
2. Review this README thoroughly
3. Open a new issue with detailed description

---

**Built with ❤️ for the LangGraph community**