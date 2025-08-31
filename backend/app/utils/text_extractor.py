import pdfplumber  # Alternative to PyMuPDF
from typing import List
import re

class TextExtractor:
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    async def extract_text(self, file_path: str) -> List[str]:
        """Extract text from PDF and split into chunks"""
        try:
            # Open PDF with pdfplumber
            with pdfplumber.open(file_path) as pdf:
                text = ""
                
                # Extract text from all pages
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            # Clean text
            text = self._clean_text(text)
            
            # Split into chunks
            chunks = self._split_text(text)
            
            return chunks
            
        except Exception as e:
            print(f"Error extracting text from {file_path}: {str(e)}")
            return []
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}]', '', text)
        
        return text.strip()
    
    def _split_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks"""
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings
                for i in range(end, max(start + self.chunk_size - 100, start), -1):
                    if text[i] in '.!?':
                        end = i + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - self.overlap
            if start >= len(text):
                break
        
        return chunks
