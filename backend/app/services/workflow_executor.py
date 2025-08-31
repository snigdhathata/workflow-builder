from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from app.models.workflow import Workflow, WorkflowComponent
from app.models.chat import ChatSession
from app.services.chat_service import ChatService
from app.utils.embedding_service import EmbeddingService
from app.utils.llm_service import LLMService
from app.utils.web_search_service import WebSearchService

class WorkflowExecutor:
    def __init__(self, db: Session):
        self.db = db
        self.chat_service = ChatService(db)
        self.embedding_service = EmbeddingService()
        self.llm_service = LLMService()
        self.web_search_service = WebSearchService()
    
    async def execute_workflow(self, session_id: int, user_query: str) -> Dict[str, Any]:
        """Execute a workflow for a given user query"""
        # Get chat session and workflow
        session = await self.chat_service.get_session(session_id)
        if not session:
            raise ValueError("Chat session not found")
        
        workflow = self.db.query(Workflow).filter(Workflow.id == session.workflow_id).first()
        if not workflow:
            raise ValueError("Workflow not found")
        
        # Get workflow components
        components = self.db.query(WorkflowComponent).filter(
            WorkflowComponent.workflow_id == workflow.id
        ).all()
        
        # Execute workflow components in order
        context = {"user_query": user_query}
        
        # Find and execute components in the correct order
        # This is a simplified execution - in a real implementation,
        # you'd want to follow the actual connections between components
        
        for component in components:
            if component.component_type == "user_query":
                # User query component - already handled
                continue
            elif component.component_type == "knowledge_base":
                context = await self._execute_knowledge_base(component, context)
            elif component.component_type == "llm_engine":
                context = await self._execute_llm_engine(component, context)
            elif component.component_type == "output":
                # Output component - final response
                return context
        
        # If no output component found, return the last context
        return context
    
    async def _execute_knowledge_base(self, component: WorkflowComponent, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute knowledge base component"""
        config = component.configuration or {}
        
        # Search for relevant documents
        query = context.get("user_query", "")
        search_results = await self.embedding_service.search_similar(
            query, 
            n_results=config.get("max_results", 5)
        )
        
        # Extract relevant context
        relevant_context = "\n".join([result['text'] for result in search_results])
        
        context["knowledge_context"] = relevant_context
        context["search_results"] = search_results
        
        return context
    
    async def _execute_llm_engine(self, component: WorkflowComponent, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute LLM engine component"""
        config = component.configuration or {}
        
        # Prepare prompt
        user_query = context.get("user_query", "")
        knowledge_context = context.get("knowledge_context", "")
        
        # Build prompt based on configuration
        if knowledge_context:
            prompt = f"""Context: {knowledge_context}

Question: {user_query}

Please answer the question based on the provided context."""
        else:
            prompt = user_query
        
        # Get LLM configuration
        llm_provider = config.get("llm_provider", "openai")
        model = config.get("model", "gpt-3.5-turbo")
        custom_prompt = config.get("custom_prompt", "")
        
        if custom_prompt:
            prompt = custom_prompt.replace("{query}", user_query).replace("{context}", knowledge_context)
        
        # Execute LLM
        response = await self.llm_service.generate_response(
            prompt=prompt,
            provider=llm_provider,
            model=model,
            max_tokens=config.get("max_tokens", 1000)
        )
        
        # Check if web search is enabled
        if config.get("enable_web_search", False):
            web_results = await self.web_search_service.search(user_query)
            context["web_results"] = web_results
        
        context["response"] = response
        return context


