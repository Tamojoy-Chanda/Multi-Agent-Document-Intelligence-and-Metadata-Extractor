from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from pdf_utils import extract_text_from_pdf_bytes
from agents import process_document_text
from db import insert_document_metadata, get_all_documents

app = FastAPI(title="Multi-Agent Document Intelligence API")

# Allow CORS for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    # Read file content
    contents = await file.read()
    
    # Extract text
    text = extract_text_from_pdf_bytes(contents)
    if not text:
        raise HTTPException(status_code=500, detail="Could not extract text from the PDF.")
    
    # Process text through Multi-Agent Workflow
    try:
        agent_result = process_document_text(text)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Agent workflow failed: {str(e)}")
    
    # Save to database
    doc_id = insert_document_metadata(
        filename=file.filename,
        category=agent_result['category'],
        metadata=agent_result['metadata']
    )
    
    return {
        "id": doc_id,
        "filename": file.filename,
        "category": agent_result['category'],
        "metadata": agent_result['metadata'],
        "message": "Document processed and saved successfully."
    }

@app.get("/api/documents")
async def get_documents():
    docs = get_all_documents()
    return docs

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
