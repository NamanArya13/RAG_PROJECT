from services.embeddings import EmbeddingService
from core.storage import VectorStore
from core.storage import ParentStore


embedder = EmbeddingService()
vector_store = VectorStore()
parent_store = ParentStore()


def query_rag(query: str):
    # Step 1: Embed query
    query_embedding = embedder.embed([query])

    # Step 2: Search child chunks
    results = vector_store.search(query_embedding, k=10)

    # Step 3: Collect parent IDs
    parent_ids = set()
    for r in results:
        parent_ids.add(r["parent_id"])

    # Step 4: Fetch parent chunks
    parent_chunks = parent_store.get(list(parent_ids)[:5])

    # Step 5: Build context
    context = "\n\n".join(parent_chunks)

    return context