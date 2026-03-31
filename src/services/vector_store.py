import logging

import faiss
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStore:

    def __init__(self, dim=384):
        self.index = faiss.IndexFlatL2(dim)
        self.texts_store = []
        self.metadata_store = []

    def add(self, embeddings, texts, metadatas):
        self.index.add(np.array(embeddings).astype("float32"))

        for text, meta in zip(texts, metadatas):
            self.texts_store.append(text)
            self.metadata_store.append(meta)
        
        logging.info("Added %d embeddings to vector store. Total stored embeddings: %d %d", len(embeddings), len(self.texts_store),len(self.metadata_store))

    def search(self, query_embedding, k=3):
        query_embedding = np.array(query_embedding).astype("float32")
        logger.info(f"Query shape: {query_embedding.shape}")
        logger.info(f"Index total vectors: {self.index.ntotal}")
        D, I = self.index.search(query_embedding, k)

        logger.info(f"Indices: {I}")
        logger.info(f"Distances: {D}")

        results = []
        for i, idx in enumerate(I[0]):

            if idx == -1 or idx >= len(self.texts_store):
                continue  
            if idx < len(self.texts_store):
                metadata = self.metadata_store[idx]
                results.append({
            'text': self.texts_store[idx],
            'metadata': metadata,
            'score': float(D[0][i]),
            'parent_id': metadata.get("parent_id")
             })

        return results