import requests
from typing import List, Dict, Any
from app.core.config import settings

class WebSearchService:
    def __init__(self):
        self.api_key = settings.SERPAPI_API_KEY
        self.base_url = "https://serpapi.com/search"
    
    async def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search the web using SerpAPI"""
        if not self.api_key:
            raise ValueError("SerpAPI key not configured")
        
        try:
            params = {
                "q": query,
                "api_key": self.api_key,
                "num": num_results,
                "engine": "google"
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract search results
            results = []
            if "organic_results" in data:
                for result in data["organic_results"][:num_results]:
                    results.append({
                        "title": result.get("title", ""),
                        "snippet": result.get("snippet", ""),
                        "link": result.get("link", ""),
                        "position": result.get("position", 0)
                    })
            
            return results
            
        except Exception as e:
            print(f"Error performing web search: {str(e)}")
            return []
    
    async def search_news(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search for news using SerpAPI"""
        if not self.api_key:
            raise ValueError("SerpAPI key not configured")
        
        try:
            params = {
                "q": query,
                "api_key": self.api_key,
                "num": num_results,
                "engine": "google",
                "tbm": "nws"  # News search
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract news results
            results = []
            if "news_results" in data:
                for result in data["news_results"][:num_results]:
                    results.append({
                        "title": result.get("title", ""),
                        "snippet": result.get("snippet", ""),
                        "link": result.get("link", ""),
                        "date": result.get("date", ""),
                        "source": result.get("source", "")
                    })
            
            return results
            
        except Exception as e:
            print(f"Error performing news search: {str(e)}")
            return []


