import logging
from src.services.embeddings import EmbeddingService
from src.core.storage import vector_store, parent_store
from fastapi import APIRouter
from pydantic import BaseModel
import numpy as np
from src.services.llm_service import LLMService


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
llm = LLMService()

router = APIRouter(prefix="/query", tags=["Query"])

class QueryRequest(BaseModel):
    query: str

embedder = EmbeddingService()

@router.post("/")
def query_rag(query: QueryRequest):
    # Step 1: Embed query
    query_embedding = embedder.embed([query.query])
    query_embedding = np.array(query_embedding).astype("float32").reshape(1, -1)

    # Step 2: Search child chunks
    results = vector_store.search(query_embedding, k=10)
    logger.info("Search results for query %r: %s", query.query, results)

    # Step 3: Collect parent IDs
    parent_ids = set()
    for r in results:
        parent_ids.add(r["parent_id"])

    # Step 4: Fetch parent chunks
    parent_chunks = parent_store.get(list(parent_ids)[:5])

    # Step 5: Build context
    context = "\n\n".join(parent_chunks)

    prompt = f"""
    Answer the question based only on the context below.

    Context:
    {context}

    Question:
    {query.query}
    """

    answer = llm.generate(prompt)

    return answer