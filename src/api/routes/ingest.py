from src.utils.chunker import Chunker
from src.services.embeddings import EmbeddingService
from src.core.storage import vector_store, parent_store
import uuid
from fastapi import APIRouter
from pydantic import BaseModel
from src.utils.loader import DocumentLoader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ingest", tags=["Ingest"])

class IngestRequest(BaseModel):
    source: str   # file path OR URL
    file_type: str  # pdf | docx | url


chunker = Chunker()
embedder = EmbeddingService()

@router.post("/")
def ingest_document(req: IngestRequest):
    doc_id = str(uuid.uuid4())
    
    text = DocumentLoader.load(req.source, req.file_type)

    logger.info("Loaded document %r with length %d characters", req.source, len(text))

    parents, children = chunker.chunk(text, doc_id)

    # Store parents
    parent_store.add(parents)

    # Embed children
    child_texts = [c["text"] for c in children]
    
    logger.info("child text = %s", child_texts[0])
    embeddings = embedder.embed(child_texts)

    logger.info("total embeddings created for document %r: %d", req.source, len(embeddings))


    metadatas = [
        {
        "chunk_id": child["chunk_id"],
        "parent_id": child["parent_id"],
        "doc_id": child["doc_id"]
        }
    for child in children
    ]

    logger.info("Prepared metadata for %d child chunks of document %r", len(metadatas), req.source)

    # Store in vector DB
    vector_store.add(embeddings, child_texts, metadatas)

    return {"status": "success", "doc_id": doc_id}