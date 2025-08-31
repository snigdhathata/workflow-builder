from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models.workflow import Workflow, WorkflowComponent
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate, WorkflowComponentCreate, WorkflowComponentUpdate

class WorkflowService:
    def __init__(self, db: Session):
        self.db = db
    
    async def create_workflow(self, workflow: WorkflowCreate) -> Workflow:
        """Create a new workflow"""
        db_workflow = Workflow(**workflow.dict())
        self.db.add(db_workflow)
        self.db.commit()
        self.db.refresh(db_workflow)
        return db_workflow
    
    async def get_workflows(self, skip: int = 0, limit: int = 100) -> List[Workflow]:
        """Get all workflows"""
        return self.db.query(Workflow).offset(skip).limit(limit).all()
    
    async def get_workflow(self, workflow_id: int) -> Optional[Workflow]:
        """Get a specific workflow by ID"""
        return self.db.query(Workflow).filter(Workflow.id == workflow_id).first()
    
    async def update_workflow(self, workflow_id: int, workflow: WorkflowUpdate) -> Optional[Workflow]:
        """Update a workflow"""
        db_workflow = await self.get_workflow(workflow_id)
        if not db_workflow:
            return None
        
        update_data = workflow.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_workflow, field, value)
        
        self.db.commit()
        self.db.refresh(db_workflow)
        return db_workflow
    
    async def delete_workflow(self, workflow_id: int) -> bool:
        """Delete a workflow"""
        db_workflow = await self.get_workflow(workflow_id)
        if not db_workflow:
            return False
        
        self.db.delete(db_workflow)
        self.db.commit()
        return True
    
    async def add_component(self, workflow_id: int, component: WorkflowComponentCreate) -> WorkflowComponent:
        """Add a component to a workflow"""
        db_component = WorkflowComponent(**component.dict(), workflow_id=workflow_id)
        self.db.add(db_component)
        self.db.commit()
        self.db.refresh(db_component)
        return db_component
    
    async def update_component(self, workflow_id: int, component_id: int, component: WorkflowComponentUpdate) -> Optional[WorkflowComponent]:
        """Update a workflow component"""
        db_component = self.db.query(WorkflowComponent).filter(
            WorkflowComponent.id == component_id,
            WorkflowComponent.workflow_id == workflow_id
        ).first()
        
        if not db_component:
            return None
        
        update_data = component.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_component, field, value)
        
        self.db.commit()
        self.db.refresh(db_component)
        return db_component
    
    async def delete_component(self, workflow_id: int, component_id: int) -> bool:
        """Delete a workflow component"""
        db_component = self.db.query(WorkflowComponent).filter(
            WorkflowComponent.id == component_id,
            WorkflowComponent.workflow_id == workflow_id
        ).first()
        
        if not db_component:
            return False
        
        self.db.delete(db_component)
        self.db.commit()
        return True
    
    async def validate_workflow(self, workflow_id: int) -> Dict[str, Any]:
        """Validate a workflow configuration"""
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return {"valid": False, "error": "Workflow not found"}
        
        components = self.db.query(WorkflowComponent).filter(
            WorkflowComponent.workflow_id == workflow_id
        ).all()
        
        # Check if workflow has required components
        component_types = [comp.component_type for comp in components]
        
        if "user_query" not in component_types:
            return {"valid": False, "error": "Missing User Query component"}
        
        if "output" not in component_types:
            return {"valid": False, "error": "Missing Output component"}
        
        # Check if there's a path from user_query to output
        # This is a simplified validation - in a real implementation,
        # you'd want to check for actual connections between components
        
        return {
            "valid": True,
            "workflow_id": workflow_id,
            "component_count": len(components),
            "components": component_types
        }


