import os
from dotenv import load_dotenv
load_dotenv()

# Langchain tracing exports
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("Langsmith_api")
os.environ["LANGSMITH_PROJECT"] = "flashcard_rag_backend"

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_dir = "./chroma_db"

embeddings_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def get_vectorstore(deck_id):
    deck_path = os.path.join(CHROMA_dir, deck_id)
    os.makedirs(deck_path, exist_ok=True)
    return Chroma(persist_directory=deck_path, embedding_function=embeddings_function)

from langchain_text_splitters import RecursiveCharacterTextSplitter

def add_documents(deck_id: str, docs: list[str]):
    splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    splits = []
    for doc in docs:
        splits.extend(splitter.split_text(doc))
    vectorstore = get_vectorstore(deck_id)
    vectorstore.add_texts(splits)
    
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2:3B")

from langchain.chains import RetrievalQA

def ask_question(deck_id: str, question: str):
    vectorstore = get_vectorstore(deck_id)
    retriever = vectorstore.as_retriever()
    qa = RetrievalQA.from_chain_type(
        llm = llm,
        retriever = retriever,
        return_source_documents = True
    )
    result = qa({"query": question})
    return {
        "answer": result["result"],
        "sources": [doc.page_content for doc in result["source_documents"]]
    }
    
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
    
def ask_MCQ(deck_id: str, question: str):
    vectorstore = get_vectorstore(deck_id)
    retriever = vectorstore.as_retriever()
    docs = retriever.get_relevant_documents(question)
    context = "\n".join([d.page_content for d in docs])
    prompt = PromptTemplate(
    template="""
    You are an assistant that creates multiple choice questions (MCQs) based strictly on the given context.

    Context:
    {context}

    Question:
    {question}

    Task:
    1. Identify the correct answer from the context.
    2. Generate 3 plausible but incorrect distractors.
    3. Shuffle the order so the correct answer is not always first.
    4. Return the result as strict JSON with exactly these fields:
       - "answer": (integer, the correct answer option number),
       - "options": (list of 4 strings, including the correct answer),
       - "sources": (list of strings, copy directly from the provided context chunks).

    Output ONLY valid JSON, nothing else.
    """,
    input_variables=["context", "question"]
)
    
    chain = LLMChain(llm = llm, prompt = prompt)
    raw_output = chain.run({"context": context, "question": question})
    try:
        mcq = json.loads(raw_output)
    except Exception:
        mcq = {"error": "Failed to parse LLM output", "raw": raw_output}
    
    print(raw_output)
    return mcq