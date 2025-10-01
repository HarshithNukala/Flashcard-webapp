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
    # vectorstore = get_vectorstore(deck_id)
    # retriever = vectorstore.as_retriever()
    # qa = RetrievalQA.from_chain_type(
    #     llm = llm,
    #     retriever = retriever,
    #     return_source_documents = True
    # )
    # result = qa({"query": question})
    # return {
    #     "answer": result["result"],
    #     "sources": [doc.page_content for doc in result["source_documents"]]
    # }
    result = llm.invoke(question)
    return {
        "answer": result.content,
        "sources": ["test sources"]
    }