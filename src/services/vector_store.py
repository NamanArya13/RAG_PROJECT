import faiss
import numpy as np


class VectorStore:

    def __init__(self, dim=384):
        self.index = faiss.IndexFlatL2(dim)
        self.texts_store = []
        self.metadata_store = []

    def add(self, embeddings, texts, metadatas):
        self.index.add(np.array(embeddings))

        for text, meta in zip(texts, metadatas):
            self.texts_store.append(text)
            self.metadata_store.append(meta)

    def search(self, query_embedding, k=10):
        D, I = self.index.search(np.array([query_embedding]), k)

        results = []
        for idx in I[0]:
            if idx < len(self.texts_store):
                results.append({
                    'text': self.texts_store[idx],
                    'metadata': self.metadata_store[idx],
                    'score': float(D[0][list(I[0]).index(idx)])
                })

        return results