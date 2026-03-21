from fastapi import FastAPI
from src.api.routes import health

app = FastAPI(title="AI RAG Platform")

app.include_router(health.router)

@app.get("/")
def root():
    return {"message": "RAG System Running"}