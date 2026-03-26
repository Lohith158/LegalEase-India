from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn
import os
from app import rag
from app import safety
from app import logger
from pydantic import BaseModel
from contextlib import asynccontextmanager
from langchain_core.documents import Document

vectorstore = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global vectorstore
    documents = rag.load_documents()
    vectorstore = rag.create_vectorstore(documents)
    yield

app = FastAPI(lifespan=lifespan)


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
    search_results = rag.search(request.question, vectorstore)
    source = list(set([os.path.basename(result.metadata["source"]) for result in search_results]))
    answer = rag.get_answer(request.question, vectorstore)
    logger.log_collection(request.question, answer, source)
    return {"answer": answer, "source": source}

@app.post("/upload")
async def upload(file: UploadFile=File(...)):
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
    url_text = rag.load_url(request.url)
    doc = Document(page_content=url_text)
    vectorstore.add_documents([doc])
    return {"message": "uploaded successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)