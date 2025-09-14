import google.generativeai as genai
from typing import Optional
import asyncio
from app.core.config import settings

class GeminiService:
    def __init__(self):
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    async def generate_review(self, system_prompt: str, user_prompt: str) -> str:
        """Generate code review using Gemini"""
        if not self.model:
            return "Gemini API key not configured. Please set GEMINI_API_KEY environment variable."
        
        try:
            # Combine system and user prompts
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            # Generate response
            response = await asyncio.to_thread(
                self.model.generate_content,
                full_prompt
            )
            
            return response.text
        except Exception as e:
            return f"Error generating review: {str(e)}"
    
    async def generate_summary(self, text: str) -> str:
        """Generate a summary of the given text"""
        if not self.model:
            return "Gemini API key not configured."
        
        try:
            prompt = f"Please provide a concise summary of the following text:\n\n{text}"
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def is_configured(self) -> bool:
        """Check if Gemini is properly configured"""
        return self.model is not None
