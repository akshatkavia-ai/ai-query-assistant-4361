#!/bin/bash
# Backend Server Startup Script
# This script starts the FastAPI backend server on port 3001

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=================================================="
echo "Starting AI Query Assistant Backend"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found."
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found."
    echo "Creating .env from .env.example if available..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Please edit .env file with your configuration."
    else
        echo "Error: No .env.example found. Please create .env file manually."
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

echo ""
echo "Configuration:"
echo "  - Host: 0.0.0.0"
echo "  - Port: 3001"
echo "  - Environment: Development"
echo ""
echo "Endpoints:"
echo "  - Health: http://localhost:3001/health"
echo "  - API Docs: http://localhost:3001/docs"
echo "  - OpenAPI: http://localhost:3001/openapi.json"
echo ""
echo "=================================================="
echo ""

# Start the server
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
