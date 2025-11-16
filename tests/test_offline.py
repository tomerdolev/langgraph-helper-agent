import pytest
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.offline_mode import load_offline_docs
from agent.retrieval import OfflineRetriever


def test_load_offline_docs_exists():
    """Test that load_offline_docs returns a string"""
    docs = load_offline_docs()
    assert isinstance(docs, str)


def test_retriever_with_sample_data(tmp_path):
    """Test OfflineRetriever with sample data"""
    # Create sample .txt files
    doc1 = tmp_path / "doc1.txt"
    doc1.write_text("StateGraph is used for state management in LangGraph")
    
    doc2 = tmp_path / "doc2.txt"
    doc2.write_text("MessageGraph is used for handling messages")
    
    doc3 = tmp_path / "doc3.txt"
    doc3.write_text("LangChain provides tools for building LLM applications")
    
    # Initialize retriever
    retriever = OfflineRetriever(tmp_path)
    
    # Test search functionality
    results = retriever.search("state management", top_k=2)
    
    assert len(results) <= 2, "Should return at most top_k results"
    assert len(results) > 0, "Should return at least one result"


def test_retriever_returns_correct_number_of_results(tmp_path):
    """Test that retriever respects top_k parameter"""
    # Create 5 sample files
    for i in range(5):
        doc = tmp_path / f"doc{i}.txt"
        doc.write_text(f"Document {i} about LangGraph and agents")
    
    retriever = OfflineRetriever(tmp_path)
    
    # Test different top_k values
    results_3 = retriever.search("LangGraph", top_k=3)
    assert len(results_3) <= 3
    
    results_5 = retriever.search("agents", top_k=5)
    assert len(results_5) <= 5


def test_retriever_handles_empty_query(tmp_path):
    """Test that retriever handles empty queries gracefully"""
    doc = tmp_path / "doc.txt"
    doc.write_text("Sample content")
    
    retriever = OfflineRetriever(tmp_path)
    results = retriever.search("", top_k=1)
    
    # Should return something even with empty query
    assert isinstance(results, list)
    assert len(results) >= 1