from pydantic import BaseModel
from typing import List, Optional

class QuestionRequest(BaseModel):
    deck_id: str
    question: str
    
class AnswerResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None
    
class DocumentRequest(BaseModel):
    deck_id: str
    docs: List[str]