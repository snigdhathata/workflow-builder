from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ChatSessionBase(BaseModel):
    workflow_id: int
    session_name: str

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSessionResponse(ChatSessionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatMessageBase(BaseModel):
    role: str
    content: str
    message_metadata: Optional[Dict[str, Any]] = None

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageResponse(ChatMessageBase):
    id: int
    session_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

