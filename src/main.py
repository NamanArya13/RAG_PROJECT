from fastapi import FastAPI
from src.api.routes import health
from src.api.routes import ingest
from src.api.routes import query

app = FastAPI(title="AI RAG Platform")

app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(query.router)

@app.get("/")
def root():
    return {"message": "RAG System Running"}