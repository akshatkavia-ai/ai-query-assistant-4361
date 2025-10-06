#!/bin/bash
# Backend Server Production Startup Script
# This script starts the FastAPI backend with Gunicorn for production use

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=================================================="
echo "Starting AI Query Assistant Backend (Production)"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found."
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found."
    echo "Please create .env file with required environment variables."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if gunicorn is installed
if ! command -v gunicorn &> /dev/null; then
    echo "Installing gunicorn..."
    pip install gunicorn
fi

# Configuration
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-3001}"
WORKERS="${WORKERS:-4}"
WORKER_CLASS="uvicorn.workers.UvicornWorker"

echo ""
echo "Configuration:"
echo "  - Host: $HOST"
echo "  - Port: $PORT"
echo "  - Workers: $WORKERS"
echo "  - Worker Class: $WORKER_CLASS"
echo ""
echo "Endpoints:"
echo "  - Health: http://localhost:$PORT/health"
echo "  - API Docs: http://localhost:$PORT/docs"
echo "  - OpenAPI: http://localhost:$PORT/openapi.json"
echo ""
echo "=================================================="
echo ""

# Start the server with Gunicorn
exec gunicorn src.api.main:app \
    --workers "$WORKERS" \
    --worker-class "$WORKER_CLASS" \
    --bind "$HOST:$PORT" \
    --access-logfile - \
    --error-logfile - \
    --log-level info
