import openai
import google.generativeai as genai
from typing import Optional
from app.core.config import settings

class LLMService:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
    
    async def generate_response(
        self, 
        prompt: str, 
        provider: str = "openai", 
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 1000
    ) -> str:
        """Generate response using specified LLM provider"""
        if provider.lower() == "openai":
            return await self._generate_openai_response(prompt, model, max_tokens)
        elif provider.lower() == "gemini":
            return await self._generate_gemini_response(prompt, model)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    async def _generate_openai_response(self, prompt: str, model: str, max_tokens: int) -> str:
        """Generate response using OpenAI"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")
        
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating OpenAI response: {str(e)}")
            raise
    
    async def _generate_gemini_response(self, prompt: str, model: str) -> str:
        """Generate response using Gemini"""
        if not settings.GEMINI_API_KEY:
            raise ValueError("Gemini API key not configured")
        
        try:
            # Use default model if not specified
            if not model or model == "default":
                model = "gemini-pro"
            
            gen_model = genai.GenerativeModel(model)
            response = gen_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating Gemini response: {str(e)}")
            raise


