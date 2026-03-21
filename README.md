# AI RAG Platform

This is an enterprise-grade Agentic Retrieval-Augmented Generation (RAG) system designed for scalable AI capabilities.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment variables in `config/.env`
3. Run the application: `uvicorn src.app:app --reload`

## Features

- Document ingestion (PDF, DOCX, TXT, URLs)
- Vector storage with Pinecone
- Agentic workflows with LangGraph
- FastAPI for API layer
- Kubernetes deployment

## Architecture

[Describe architecture here]