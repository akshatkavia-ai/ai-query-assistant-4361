import os
import google.generativeai as genai

# Get API key from environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Only configure if key is present (allows OpenAPI generation without key)
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

# PUBLIC_INTERFACE
def generate_answer(question: str, timeout: int = 30) -> str:
    """
    Generate an answer to a question using the Gemini API.
    
    Args:
        question: The user's question text
        timeout: Maximum time to wait for response in seconds (default: 30)
    
    Returns:
        str: The AI-generated answer
        
    Raises:
        ValueError: If GEMINI_API_KEY is not configured
        Exception: If the API call fails or times out
    """
    # Validate API key at runtime
    if not GEMINI_API_KEY or model is None:
        raise ValueError(
            "GEMINI_API_KEY environment variable is required. "
            "Please set it in your .env file or environment."
        )
    
    try:
        # Generate content with timeout
        response = model.generate_content(
            question,
            request_options={'timeout': timeout}
        )
        
        if not response or not response.text:
            raise Exception("Empty response from Gemini API")
            
        return response.text
        
    except ValueError:
        # Re-raise ValueError for missing API key
        raise
    except Exception as e:
        # Re-raise with more context
        raise Exception(f"Gemini API error: {str(e)}")
