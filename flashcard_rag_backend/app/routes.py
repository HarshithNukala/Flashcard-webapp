from fastapi import APIRouter
from .schemas import QuestionRequest, QNAAnswerResponse, MCQAnswerResponse, DocumentRequest
from .rag import ask_question, ask_MCQ, add_documents

router = APIRouter(prefix = "/rag", tags=["RAG"])

@router.get("/health")
def health_check():
    return {"Status": "OK"}

@router.post("/ask_QNA", response_model=QNAAnswerResponse)
def ask_QNA_question_endpoint(payload: QuestionRequest):
    result = ask_question(payload.deck_id, payload.question)
    return QNAAnswerResponse(answer=result["answer"], sources=result["sources"])

@router.post("/ask_MCQ", response_model=MCQAnswerResponse)
def ask_MCQ_question_endpoint(payload: QuestionRequest):
    result = ask_MCQ(payload.deck_id, payload.question)
    return MCQAnswerResponse(answer=result["answer"], options=result["options"], sources=result["sources"])

@router.post("/add_docs")
def add_docs(payload: DocumentRequest):
    add_documents(payload.deck_id, payload.docs)
    return {"message": f"Added {len(payload.docs)} documents to deck {payload.deck_id}"}