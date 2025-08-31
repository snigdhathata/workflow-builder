import os
import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.document import Document
from app.schemas.document import DocumentCreate
from app.core.config import settings
from app.utils.text_extractor import TextExtractor
from app.utils.embedding_service import EmbeddingService

class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.text_extractor = TextExtractor()
        self.embedding_service = EmbeddingService()
    
    async def upload_document(self, file: UploadFile) -> Document:
        """Upload and store a document"""
        # Create upload directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Create document record
        document_data = DocumentCreate(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=len(content),
            file_type=file.content_type or "application/pdf"
        )
        
        db_document = Document(**document_data.dict())
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        
        return db_document
    
    async def get_documents(self, skip: int = 0, limit: int = 100) -> List[Document]:
        """Get all documents"""
        return self.db.query(Document).offset(skip).limit(limit).all()
    
    async def get_document(self, document_id: int) -> Optional[Document]:
        """Get a specific document by ID"""
        return self.db.query(Document).filter(Document.id == document_id).first()
    
    async def delete_document(self, document_id: int) -> bool:
        """Delete a document"""
        db_document = await self.get_document(document_id)
        if not db_document:
            return False
        
        # Delete file from filesystem
        if os.path.exists(db_document.file_path):
            os.remove(db_document.file_path)
        
        # Delete from database
        self.db.delete(db_document)
        self.db.commit()
        return True
    
    async def process_document(self, document_id: int) -> bool:
        """Process a document to extract text and generate embeddings"""
        db_document = await self.get_document(document_id)
        if not db_document:
            return False
        
        try:
            # Extract text from PDF
            text_chunks = await self.text_extractor.extract_text(db_document.file_path)
            
            # Generate embeddings
            embeddings = await self.embedding_service.generate_embeddings(text_chunks)
            
            # Store embeddings in ChromaDB
            await self.embedding_service.store_embeddings(
                document_id=document_id,
                texts=text_chunks,
                embeddings=embeddings
            )
            
            # Update document status
            db_document.is_processed = True
            db_document.embedding_count = len(text_chunks)
            self.db.commit()
            
            return True
            
        except Exception as e:
            print(f"Error processing document {document_id}: {str(e)}")
            return False


