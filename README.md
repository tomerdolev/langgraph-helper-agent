LangGraph Helper Agent
Overview

The LangGraph Helper Agent is a Python-based assistant designed to help developers work with LangGraph and LangChain.
It answers practical questions, explains concepts, and provides examples and architectural guidance.

The agent supports two fully functional modes:

Offline Mode — Uses local documentation files, no internet required (except Gemini API).

Online Mode — Fetches real-time information using free-tier search APIs.

This project demonstrates dual-mode LLM operation, documentation retrieval, and portable system architecture.

Features
Dual Operating Modes

Offline:
Uses local llms.txt files stored in the data/ folder.
Enables work without external web access.

Online:
Uses free-tier search (DuckDuckGo) to fetch up-to-date LangGraph/LangChain info.

Mode selection is done via:

CLI flag (--mode)

OR environment variable (AGENT_MODE)

Gemini LLM Integration

Uses the Google Gemini API (free tier).

Model is fully configurable through .env.

Extensible Architecture

Clear node-based design inspired by LangGraph.

Easy to extend with more tools, retrievers, or memory components.

Modular code structure.

Portable & Easy to Run

Works on any machine with Python 3.10+

Fully documented

Dependencies managed via requirements.txt

Project Structure
langgraph-helper-agent/
│
├── main.py
├── requirements.txt
├── README.md
├── .env.example
│
├── data/
│   ├── langgraph-llms.txt
│   ├── langgraph-llms-full.txt
│   ├── langchain-llms.txt
│   └── (optional additional offline files)
│
└── src/
    ├── agent.py
    ├── mode_offline.py
    ├── mode_online.py
    ├── utils.py

Installation and Setup
1. Clone the Repository
git clone https://github.com/tomerdolev/langgraph-helper-agent.git
cd langgraph-helper-agent

2. Create a Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate


Mac/Linux

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Create a .env File

Copy from the template:

GEMINI_API_KEY=your_api_key_here
AGENT_MODE=offline   # or online

Operating Modes
Offline Mode (Required)

This mode loads local documentation files and does not rely on any internet resources (except for Gemini API requests).

How Offline Mode Works

Loads .txt documentation files from /data

Performs local search over those files

Retrieves relevant snippets

Sends augmented prompt to Gemini for final synthesis

Run
python main.py --mode offline "How do I add persistence to a LangGraph agent?"


OR using environment variable:

export AGENT_MODE=offline   # Mac/Linux
set AGENT_MODE=offline      # Windows PowerShell
python main.py "Explain checkpointers."

Updating Offline Data

Users may refresh the /data folder manually:

Sources:

https://langchain-ai.github.io/langgraph/llms.txt

https://langchain-ai.github.io/langgraph/llms-full.txt

https://python.langchain.com/llms.txt

Simply download and replace the files.

Online Mode (Required)

Uses DuckDuckGo free-tier search to gather real-time information.

How Online Mode Works

Receives user query

Performs search via the duckduckgo-search package

Extracts relevant textual results

Synthesizes answers through Gemini

Run
python main.py --mode online "What are the newest LangGraph updates?"

Architecture and Design
Graph / State-Based Structure

Even without relying on LangGraph itself, the architecture follows fundamental LangGraph concepts.

State Includes:

question — user input

mode — online/offline

retrieved_docs — contextual snippets

answer — final LLM output

Nodes:
Node	Responsibility
LoadMode	Determines online/offline state
RetrieverOffline	Searches .txt docs
RetrieverOnline	Performs web search
LLMNode	Calls Gemini API
FormatAnswer	Builds final response
Mode Resolution Order:

CLI flag

Environment variable

Default to offline

Example Questions the Agent Can Handle

“How do I add persistence to a LangGraph agent?”

“What’s the difference between StateGraph and MessageGraph?”

“Show me how to implement human-in-the-loop in LangGraph.”

“How do I handle retries in LangGraph nodes?”

“Best practices for managing state in LangGraph?”

Example Runs
Offline
python main.py --mode offline "Explain checkpointers in LangGraph."

Online
python main.py --mode online "What changed in LangChain 0.3?"

Dependencies
google-generativeai
duckduckgo-search
python-dotenv
langchain
langgraph
tqdm

Data Freshness Strategy
Offline Mode

Users update the data/ folder manually:

data/
    langgraph-llms.txt
    langgraph-llms-full.txt
    langchain-llms.txt

Online Mode

Always fetches fresh information through DuckDuckGo search.
