import chromadb
from chromadb.config import Settings
from typing import List, Optional
import openai
from app.core.config import settings

class EmbeddingService:
    def __init__(self):
        self.client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT
        )
        self.collection = self.client.get_or_create_collection("documents")
        
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
    
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for text chunks"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")
        
        try:
            response = openai.Embedding.create(
                input=texts,
                model="text-embedding-ada-002"
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            raise
    
    async def store_embeddings(self, document_id: int, texts: List[str], embeddings: List[List[float]]):
        """Store embeddings in ChromaDB"""
        try:
            # Create IDs for each chunk
            ids = [f"doc_{document_id}_chunk_{i}" for i in range(len(texts))]
            
            # Store in ChromaDB
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                ids=ids,
                metadatas=[{"document_id": document_id, "chunk_index": i} for i in range(len(texts))]
            )
        except Exception as e:
            print(f"Error storing embeddings: {str(e)}")
            raise
    
    async def search_similar(self, query: str, n_results: int = 5) -> List[dict]:
        """Search for similar documents"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")
        
        try:
            # Generate embedding for query
            query_embedding = await self.generate_embeddings([query])
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"Error searching embeddings: {str(e)}")
            raise


