import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import ask
from src.database.connection import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI app.
    Handles startup and shutdown events.
    """
    # Startup: Initialize database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: cleanup if needed

# Initialize FastAPI app with metadata
app = FastAPI(
    title="AI Q&A Backend",
    description="Backend API for AI-powered question and answer service using Gemini API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
if CORS_ORIGINS == "*":
    allowed_origins = ["*"]
else:
    allowed_origins = [origin.strip() for origin in CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ask.router)

@app.get("/", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Status message indicating the service is healthy
    """
    return {"message": "Healthy", "service": "AI Q&A Backend"}
