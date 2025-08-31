from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentBase(BaseModel):
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    file_type: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    is_processed: bool
    embedding_count: int
    created_at: datetime
    processed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


