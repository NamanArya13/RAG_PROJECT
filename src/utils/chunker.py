from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict, Tuple
import uuid


class Chunker:

    def __init__(self):
        # Parent (large context)
        self.parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200
        )

        # Child (retrieval precision)
        self.child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=250,
            chunk_overlap=50
        )

    def chunk(self, text: str, doc_id: str) -> Tuple[List[Dict], List[Dict]]:
        parents = []
        children = []

        parent_chunks = self.parent_splitter.split_text(text)

        for parent_text in parent_chunks:
            parent_id = str(uuid.uuid4())

            # Store parent
            parents.append({
                "parent_id": parent_id,
                "doc_id": doc_id,
                "text": parent_text
            })

            # Create child chunks from parent
            child_chunks = self.child_splitter.split_text(parent_text)

            for child_text in child_chunks:
                children.append({
                    "chunk_id": str(uuid.uuid4()),
                    "parent_id": parent_id,
                    "doc_id": doc_id,
                    "text": child_text
                })

        return parents, children