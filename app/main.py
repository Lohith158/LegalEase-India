from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn
import os
from app import rag
from app import safety
from app import logger
from pydantic import BaseModel
from contextlib import asynccontextmanager
from langchain_core.documents import Document
import threading
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


vectorstore = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    def init_vectorstore():
        global vectorstore
        try:
            documents = rag.load_documents()
            vectorstore = rag.create_vectorstore(documents)
            
        except Exception as e:
            vectorstore = None
            print("Vectorstore initialization failed:", e)

    thread = threading.Thread(target=init_vectorstore)
    thread.start()
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return FileResponse("app/static/index.html")


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "LegalEase India is running"}

class AskRequest(BaseModel):
    question : str

@app.post("/ask")
def asK(request: AskRequest):
    is_safe = safety.is_safe(request.question)
    if is_safe == False:
        raise HTTPException(status_code=400, detail="unsafe query")
    if vectorstore is None:
        raise HTTPException(status_code=500, detail="Legal database is currently unavailable. Please try again later.")
    search_results = rag.search(request.question, vectorstore)
    if not search_results:
        return {"answer": "No relevant legal information found for your question."}
    sources = list(set([os.path.basename(result.metadata["source"]) for result in search_results]))
    answer = rag.get_answer(request.question, vectorstore)
    if "enough information" in answer:
        return {"answer": answer, "sources": []}
    logger.log_collection(request.question, answer, sources)
    return {"answer": answer, "sources": sources}

@app.post("/upload")
async def upload(file: UploadFile=File(...)):
    if vectorstore is None:
        raise HTTPException(status_code=500, detail="Legal database is currently unavailable. Please try again later.")
    filepath = os.path.join("data/pdfs/", file.filename)
    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)
    documents = rag.load_uploaded_documents(filepath)
    vectorstore.add_documents(documents)
    return {"message": "uploaded successfully"}

class UrlRequest(BaseModel):
    url : str

@app.post("/add-url")
def add_url(request: UrlRequest):
    if vectorstore is None:
        raise HTTPException(status_code=500, detail="Legal database is currently unavailable. Please try again later.")
    url_text = rag.load_url(request.url)
    doc = Document(page_content=url_text)
    vectorstore.add_documents([doc])
    return {"message": "uploaded successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)