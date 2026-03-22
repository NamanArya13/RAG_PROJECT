from utils.chunker import Chunker
from services.embeddings import EmbeddingService
from core.storage import VectorStore
from core.storage import ParentStore
import uuid


chunker = Chunker()
embedder = EmbeddingService()
vector_store = VectorStore()
parent_store = ParentStore()


def ingest_document(text: str):
    doc_id = str(uuid.uuid4())

    parents, children = chunker.chunk(text, doc_id)

    # Store parents
    parent_store.add(parents)

    # Embed children
    child_texts = [c["text"] for c in children]
    embeddings = embedder.embed(child_texts)

    # Store in vector DB
    vector_store.add(embeddings, children)

    return {"status": "success", "doc_id": doc_id}