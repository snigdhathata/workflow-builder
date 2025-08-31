from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowUpdate(WorkflowBase):
    name: Optional[str] = None
    is_active: Optional[bool] = None

class WorkflowResponse(WorkflowBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class WorkflowComponentBase(BaseModel):
    component_type: str
    position_x: int
    position_y: int
    configuration: Optional[Dict[str, Any]] = None
    connections: Optional[List[str]] = None

class WorkflowComponentCreate(WorkflowComponentBase):
    pass

class WorkflowComponentUpdate(WorkflowComponentBase):
    component_type: Optional[str] = None
    position_x: Optional[int] = None
    position_y: Optional[int] = None

class WorkflowComponentResponse(WorkflowComponentBase):
    id: int
    workflow_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


