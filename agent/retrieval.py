from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class OfflineRetriever:
    def __init__(self, data_path: Path):
        self.docs = self._load_docs(data_path)
        
        # Add check for empty docs
        if not self.docs:
            raise ValueError(f"No .txt files found in {data_path}")
        
        # Add some useful parameters for better retrieval
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english'
        )
        self.doc_vectors = self.vectorizer.fit_transform(self.docs)

    def _load_docs(self, data_path: Path):
        docs = []
        for file in data_path.glob("*.txt"):
            docs.append(file.read_text(encoding="utf-8", errors="ignore"))
        return docs

    def search(self, query: str, top_k=3):
        # Handle empty query
        if not query.strip():
            return self.docs[:top_k]
        
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.doc_vectors).flatten()
        top_indices = scores.argsort()[-top_k:][::-1]
        return [self.docs[i] for i in top_indices]