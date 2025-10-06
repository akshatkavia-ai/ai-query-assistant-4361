"""
Gemini AI service integration.

Wrapper for Google Gemini API with error handling and timeout management.
"""

import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY not set. Gemini service will not function.")

# Configure Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


class GeminiService:
    """
    Service class for interacting with Google Gemini AI.
    
    Provides methods to generate text responses using the Gemini API
    with proper error handling and timeout management.
    """
    
    def __init__(self, model_name: str = "gemini-1.5-flash", timeout: int = 30):
        """
        Initialize Gemini service.
        
        Args:
            model_name: Name of the Gemini model to use (default: gemini-1.5-flash)
            timeout: Request timeout in seconds
        """
        self.model_name = model_name
        self.timeout = timeout
        self.model = None
        
        if GEMINI_API_KEY:
            try:
                self.model = genai.GenerativeModel(model_name)
                logger.info(f"✓ Gemini model '{model_name}' initialized successfully")
            except Exception as e:
                logger.error(f"✗ Failed to initialize Gemini model: {e}")
        else:
            logger.error("✗ Cannot initialize Gemini model: API key not provided")
    
    def generate_answer(self, question: str) -> str:
        """
        Generate an answer to a question using Gemini API.
        
        Args:
            question: The user's question
            
        Returns:
            str: The AI-generated answer
            
        Raises:
            ValueError: If API key is not configured
            Exception: If the API call fails
        """
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not configured. Please set it in your environment variables."
            )
        
        if not self.model:
            raise Exception("Gemini model is not initialized")
        
        try:
            logger.info(f"Generating answer for question: {question[:100]}...")
            
            # Generate response with timeout handling
            response = self.model.generate_content(
                question,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=2048,
                )
            )
            
            # Extract text from response
            if response and response.text:
                answer = response.text.strip()
                logger.info(f"✓ Successfully generated answer ({len(answer)} characters)")
                return answer
            else:
                logger.warning("⚠ Gemini returned empty response")
                return "I apologize, but I couldn't generate a response. Please try rephrasing your question."
                
        except Exception as e:
            logger.error(f"✗ Error generating answer with Gemini: {e}")
            
            # Provide user-friendly error messages
            if "quota" in str(e).lower():
                raise Exception("API quota exceeded. Please try again later.")
            elif "api key" in str(e).lower():
                raise Exception("Invalid API key. Please check your configuration.")
            elif "timeout" in str(e).lower():
                raise Exception("Request timeout. Please try again.")
            else:
                raise Exception(f"Failed to generate answer: {str(e)}")
    
    def is_available(self) -> bool:
        """
        Check if the Gemini service is available.
        
        Returns:
            bool: True if service is properly configured and available
        """
        return GEMINI_API_KEY is not None and self.model is not None


# Create singleton instance
gemini_service = GeminiService()


# PUBLIC_INTERFACE
def get_gemini_service() -> GeminiService:
    """
    Get the Gemini service instance.
    
    Returns:
        GeminiService: Singleton instance of the Gemini service
        
    Usage:
        service = get_gemini_service()
        answer = service.generate_answer("What is AI?")
    """
    return gemini_service
