from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict


class Chunker:

    def __init__(self):
        # Multi-level chunkers
        self.small_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=40
        )

        self.medium_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=80
        )

        self.large_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )

    def chunk(self, text: str) -> List[Dict]:
        chunks = []

        # Small chunks
        for c in self.small_splitter.split_text(text):
            chunks.append({
                "text": c,
                "chunk_type": "small",
                "chunk_size": 200
            })

        # Medium chunks
        for c in self.medium_splitter.split_text(text):
            chunks.append({
                "text": c,
                "chunk_type": "medium",
                "chunk_size": 500
            })

        # Large chunks
        for c in self.large_splitter.split_text(text):
            chunks.append({
                "text": c,
                "chunk_type": "large",
                "chunk_size": 1000
            })

        return chunks