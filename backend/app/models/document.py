from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(50), nullable=False)
    is_processed = Column(Boolean, default=False)
    embedding_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)


