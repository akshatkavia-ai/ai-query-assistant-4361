"""
Database connection module.

Provides SQLAlchemy engine with connection pooling and health checks.
"""

import os
import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create declarative base for ORM models
Base = declarative_base()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Fix common DATABASE_URL format issues
if DATABASE_URL:
    # Replace postgres:// with postgresql+psycopg2://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
        logger.info("Fixed DATABASE_URL scheme from postgres:// to postgresql+psycopg2://")

# Global engine and session factory (created lazily)
engine = None
SessionLocal = None


def create_db_engine():
    """
    Create database engine with connection pooling.
    
    Returns:
        Engine: SQLAlchemy engine or None if DATABASE_URL is not configured
    """
    global engine, SessionLocal
    
    if not DATABASE_URL:
        logger.warning("DATABASE_URL not configured. Database functionality will be disabled.")
        return None
    
    try:
        # Create engine with connection pooling and health checks
        engine = create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,  # Enable connection health checks
            pool_recycle=3600,   # Recycle connections after 1 hour
            echo=False           # Set to True for SQL query logging
        )
        
        # Create session factory
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        logger.info("Database engine created successfully")
        return engine
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        # Use NullPool for fallback (no connection pooling)
        engine = None
        SessionLocal = None
        return None


def get_db():
    """
    Get database session with automatic cleanup.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        with get_db() as db:
            result = db.execute(query)
    """
    if SessionLocal is None:
        logger.error("Database session factory not initialized")
        raise RuntimeError("Database not configured")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db_with_retry(max_retries=5, retry_delay=2):
    """
    Initialize database connection with retry logic.
    
    Args:
        max_retries: Maximum number of connection attempts
        retry_delay: Delay in seconds between retries
        
    Returns:
        bool: True if connection successful, False otherwise
    """
    # Create engine if not already created
    if engine is None:
        create_db_engine()
    
    # If still no engine (DATABASE_URL not configured), return False
    if engine is None:
        logger.warning("⚠ Cannot initialize database: DATABASE_URL not configured")
        return False
    
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Attempting database connection (attempt {attempt}/{max_retries})...")
            
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info("✓ Database connection established successfully!")
            return True
            
        except Exception as e:
            logger.error(f"✗ Database connection failed (attempt {attempt}/{max_retries}): {e}")
            
            if attempt < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Maximum retry attempts reached. Database connection failed.")
                return False
    
    return False


def get_db_session():
    """
    Dependency for FastAPI routes to get database session.
    
    Yields:
        Session: SQLAlchemy database session that is automatically closed
        
    Usage in FastAPI route:
        @app.post("/endpoint")
        def endpoint(db: Session = Depends(get_db_session)):
            # Use db session
            pass
    """
    # Lazy initialization of engine
    if engine is None:
        create_db_engine()
    
    if SessionLocal is None:
        logger.error("Database session factory not initialized. DATABASE_URL may be missing.")
        raise RuntimeError(
            "Database not configured. Please set DATABASE_URL environment variable."
        )
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize engine on module load (non-blocking)
try:
    create_db_engine()
except Exception as e:
    logger.warning(f"Failed to initialize database engine on startup: {e}")
