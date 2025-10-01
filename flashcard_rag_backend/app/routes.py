from fastapi import APIRouter
from .schemas import QuestionRequest, AnswerResponse, DocumentRequest
from .rag import ask_question, add_documents

router = APIRouter(prefix = "/rag", tags=["RAG"])

@router.get("/health")
def health_check():
    return {"Status": "OK"}

@router.post("/ask", response_model=AnswerResponse)
def ask_question_endpoint(payload: QuestionRequest):
    result = ask_question(payload.deck_id, payload.question)
    return AnswerResponse(answer=result["answer"], sources=result["sources"])

@router.post("/add_docs")
def add_docs(payload: DocumentRequest):
    add_documents(payload.deck_id, payload.docs)
    return {"message": f"Added {len(payload.docs)} documents to deck {payload.deck_id}"}