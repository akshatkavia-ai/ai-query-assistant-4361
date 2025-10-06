#!/usr/bin/env python3
"""
Database initialization script for AI Query Assistant.

This script creates the database schema by executing schema.sql.
It is idempotent and safe to run multiple times.
"""

import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_database_url():
    """Get database URL from environment variable."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError(
            "DATABASE_URL environment variable is not set. "
            "Please set it in your .env file or environment."
        )
    return database_url

def read_schema_file():
    """Read the schema.sql file."""
    schema_path = Path(__file__).parent / "schema.sql"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    
    with open(schema_path, 'r') as f:
        return f.read()

def init_database():
    """
    Initialize the database by executing schema.sql.
    This function is idempotent - safe to run multiple times.
    """
    try:
        # Get database URL
        database_url = get_database_url()
        print("Connecting to database...")
        
        # Create SQLAlchemy engine
        engine = create_engine(database_url)
        
        # Read schema SQL
        schema_sql = read_schema_file()
        print("Executing schema.sql...")
        
        # Execute schema with a connection
        with engine.connect() as connection:
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
            for statement in statements:
                connection.execute(text(statement))
            connection.commit()
        
        print("✓ Database schema initialized successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error initializing database: {e}", file=sys.stderr)
        return False

def main():
    """CLI entrypoint for the init script."""
    print("=" * 60)
    print("Database Initialization Script")
    print("=" * 60)
    
    success = init_database()
    
    if success:
        print("=" * 60)
        print("Initialization complete!")
        sys.exit(0)
    else:
        print("=" * 60)
        print("Initialization failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
