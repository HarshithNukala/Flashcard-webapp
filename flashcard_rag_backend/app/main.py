from fastapi import FastAPI
from .routes import router as rag_routes

app = FastAPI()

app.include_router(rag_routes)

@app.get("/{id}")
def printIndex(id: int):
    return {"message": f"The entered integer was: {id}"}

@app.get("/")
def index():
    return {"message": "hello world"}