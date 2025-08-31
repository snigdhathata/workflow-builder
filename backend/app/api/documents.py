from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse, DocumentCreate
from app.services.document_service import DocumentService

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a document for processing"""
    service = DocumentService(db)
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    return await service.upload_document(file)

@router.get("/", response_model=List[DocumentResponse])
async def get_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all uploaded documents"""
    service = DocumentService(db)
    return await service.get_documents(skip=skip, limit=limit)

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific document by ID"""
    service = DocumentService(db)
    document = await service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Delete a document"""
    service = DocumentService(db)
    success = await service.delete_document(document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}

@router.post("/{document_id}/process")
async def process_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Process a document to extract text and generate embeddings"""
    service = DocumentService(db)
    result = await service.process_document(document_id)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document processing started", "document_id": document_id}


