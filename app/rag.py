import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()
provider = os.getenv("LLM_PROVIDER", "ollama")

if provider == "gemini":
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
else:
    from langchain_ollama import OllamaLLM
    llm = OllamaLLM(model="llama3.2")
    
def load_documents() -> list:
    all_documents = []
    all_files = os.listdir("data/pdfs/")
    files = [file for file in all_files if file.endswith(".pdf") ]
    for f in files:
        filepath = os.path.join("data/pdfs/", f)
        document_loader = PyPDFLoader(filepath)
        all_documents.extend(document_loader.load())
    return all_documents

def load_uploaded_documents(filepath: str) -> list:
    document_loader = PyPDFLoader(filepath)
    return document_loader.load()

def load_url(url: str) -> str:
    response = requests.get(url)
    text = BeautifulSoup(response.text, "html.parser").get_text()
    return text 

def create_vectorstore(documents: list) -> Chroma:
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="paraphrase-MiniLM-L3-v2")
    return Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")

def load_vectorstore() -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name="paraphrase-MiniLM-L3-v2")
    return Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

def search(query: str, vectorstore: Chroma) -> list:
    results = vectorstore.similarity_search(query)
    return results

def get_answer(query: str, vectorstore: Chroma) -> str:
    results = search(query, vectorstore)
    context = " ".join([doc.page_content for doc in results])
    # prompt = f"Answer only from the given context. If not in context say 'i dont have enough information'. \n\nContext: {context}\n\nQuestion: {query}"
    system = SystemMessage("You are a legal assistent, answer only form the given context")
    user = HumanMessage(f"Context: {context}\n\nQuestion: {query}")
    output = llm.invoke([system, user])
    return output.content if hasattr(output, "content") else output
