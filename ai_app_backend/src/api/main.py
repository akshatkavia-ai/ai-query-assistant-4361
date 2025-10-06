"""
FastAPI application entry point.

Main application setup with CORS, route registration, and lifecycle events.
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.database.connection import init_db_with_retry
from src.api.routes import ask

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events for the FastAPI application.
    """
    # Startup
    logger.info("=" * 60)
    logger.info("Starting AI Query Assistant Backend")
    logger.info("=" * 60)
    
    # Initialize database connection with retry
    db_connected = init_db_with_retry(max_retries=5, retry_delay=2)
    if not db_connected:
        logger.warning("⚠ Starting application without database connection")
    
    logger.info("Application startup complete")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Query Assistant Backend")


# Create FastAPI application with metadata
app = FastAPI(
    title="AI Query Assistant API",
    description="""
    Backend API for AI Query Assistant application.
    
    This API allows users to ask questions and receive AI-generated answers
    powered by Google Gemini AI. All Q&A pairs are stored for history tracking.
    
    ## Features
    - Ask questions and get AI-powered answers
    - Store Q&A history in PostgreSQL database
    - RESTful API with automatic OpenAPI documentation
    
    ## Environment Variables Required
    - `DATABASE_URL`: PostgreSQL connection string
    - `GEMINI_API_KEY`: Google Gemini API key
    - `CORS_ORIGINS`: Comma-separated list of allowed origins (optional)
    """,
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {
            "name": "Health",
            "description": "Health check and status endpoints"
        },
        {
            "name": "Question Answering",
            "description": "AI-powered question answering endpoints"
        }
    ]
)

# Configure CORS
cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost:3000")
cors_origins = [origin.strip() for origin in cors_origins_env.split(",")]

# Log and print configured CORS origins for easy verification
logger.info(f"Configuring CORS with origins: {cors_origins}")
print(f"Configuring CORS with origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(ask.router)


# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["Health"],
    summary="Health check endpoint",
    description="Returns the health status of the API"
)
def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Status message indicating the service is healthy
    """
    return {
        "status": "healthy",
        "message": "AI Query Assistant API is running",
        "version": "1.0.0"
    }


# PUBLIC_INTERFACE
@app.get(
    "/health",
    tags=["Health"],
    summary="Detailed health check",
    description="Returns detailed health information about the service"
)
def detailed_health_check():
    """
    Detailed health check with service information.
    
    Returns:
        dict: Detailed health status including service availability
    """
    from src.services.gemini_service import get_gemini_service
    
    gemini_available = get_gemini_service().is_available()
    
    return {
        "status": "healthy",
        "services": {
            "api": "operational",
            "gemini": "available" if gemini_available else "unavailable"
        },
        "version": "1.0.0"
    }
