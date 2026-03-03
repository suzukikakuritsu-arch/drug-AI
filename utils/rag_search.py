# utils/rag_search.py
import numpy as np
import faiss
import json
from sentence_transformers import SentenceTransformer

with open("1600_articles.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

contents = [d["content"] for d in documents]
model = SentenceTransformer("all-MiniLM-L6-v2")

try:
    embeddings = np.load("embeddings.npy")
except FileNotFoundError:
    embeddings = model.encode(contents, convert_to_numpy=True)
    embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True)
    np.save("embeddings.npy", embeddings)

dim = embeddings.shape[1]
index = faiss.IndexHNSWFlat(dim, 32)
index.hnsw.efConstruction = 200
index.add(embeddings)

def rag_search(query, top_k=5):
    query_vec = model.encode([query])
    query_vec /= np.linalg.norm(query_vec)
    D, I = index.search(query_vec, top_k)
    results = []
    for i, idx in enumerate(I[0]):
        doc = documents[idx]
        results.append({
            "title": doc["title"],
            "content": doc["content"],
            "score": float(D[0][i])
        })
    return results
