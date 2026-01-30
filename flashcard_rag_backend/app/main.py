from fastapi import FastAPI
from .routes import router as rag_routes

app = FastAPI()

app.include_router(rag_routes)

@app.get("/")
def index():
    return {"message": "hello world"}