# AI Query Assistant - Local Setup Guide

This guide provides step-by-step instructions for setting up and running the AI Query Assistant application locally.

## Architecture Overview

The application consists of two main components:
- **Frontend (React)**: Runs on `http://localhost:3000`
- **Backend (FastAPI)**: Runs on `http://localhost:3001`

## Prerequisites

- **Python 3.9+** with pip
- **Node.js 14+** with npm
- **PostgreSQL 12+** (optional - app works without database)
- **Google Gemini API Key** (required for AI functionality)

## Quick Start

### 1. Backend Setup

```bash
# Navigate to backend directory
cd ai_app_backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set your GEMINI_API_KEY

# Start backend server
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

**Backend will be running at:** `http://localhost:3001`

### 2. Frontend Setup

```bash
# Open a new terminal and navigate to frontend directory
cd ai_app_frontend

# Install dependencies
npm install

# Configure environment (should already be correct)
# .env should contain: REACT_APP_BACKEND_URL=http://localhost:3001

# Start frontend server
npm start
```

**Frontend will be running at:** `http://localhost:3000`

### 3. Verify Setup

```bash
# In backend directory
./verify_setup.sh

# In frontend directory
./verify_setup.sh
```

## Detailed Configuration

### Backend Configuration (.env)

The backend requires these environment variables in `ai_app_backend/.env`:

```bash
# Required: Google Gemini API Key
GEMINI_API_KEY=your_actual_api_key_here

# Optional: Database connection (app works without it)
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/ai_app_db

# Required: CORS configuration for frontend
CORS_ORIGINS=http://localhost:3000
```

**Getting a Gemini API Key:**
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

### Frontend Configuration (.env)

The frontend requires only one environment variable in `ai_app_frontend/.env`:

```bash
# Backend API URL
REACT_APP_BACKEND_URL=http://localhost:3001
```

**Important:** 
- Do NOT put backend variables (GEMINI_API_KEY, DATABASE_URL) in frontend .env
- After changing .env, you MUST restart the dev server (Ctrl+C, then `npm start`)

## Port Configuration

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend | 3001 | http://localhost:3001 |
| Backend Docs | 3001 | http://localhost:3001/docs |
| Backend Health | 3001 | http://localhost:3001/health |

## Testing the Connection

### Test Backend Directly

```bash
# Health check
curl http://localhost:3001/health

# Ask a question
curl -X POST http://localhost:3001/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is artificial intelligence?"}'
```

### Test Frontend to Backend

1. Open http://localhost:3000 in your browser
2. Type a question in the input field
3. Click "Ask AI" or press Enter
4. You should see the AI-generated response

## Common Issues and Solutions

### Issue: Frontend can't connect to backend

**Symptoms:**
- "Failed to connect to backend" error
- Network errors in browser console

**Solutions:**
1. Verify backend is running: `curl http://localhost:3001/health`
2. Check frontend .env has: `REACT_APP_BACKEND_URL=http://localhost:3001`
3. Restart frontend after .env changes: Stop (Ctrl+C) and run `npm start`
4. Check CORS in backend .env includes: `CORS_ORIGINS=http://localhost:3000`

### Issue: CORS errors in browser console

**Symptoms:**
- "blocked by CORS policy" in browser console
- Requests fail with CORS errors

**Solutions:**
1. Verify backend .env has: `CORS_ORIGINS=http://localhost:3000`
2. Restart backend after changing CORS settings
3. Clear browser cache (Ctrl+Shift+R for hard refresh)

### Issue: "AI service not available"

**Symptoms:**
- 503 Service Unavailable errors
- Backend logs show Gemini API errors

**Solutions:**
1. Check backend .env has valid GEMINI_API_KEY
2. Verify API key at https://makersuite.google.com/app/apikey
3. Restart backend after updating API key
4. Check API quota hasn't been exceeded

### Issue: Port already in use

**Symptoms:**
- "Port 3000 already in use" or "Port 3001 already in use"

**Solutions:**

For port 3001 (backend):
```bash
# Find process
lsof -i :3001
# Kill it
kill -9 <PID>
```

For port 3000 (frontend):
```bash
# Find process
lsof -i :3000
# Kill it
kill -9 <PID>
```

### Issue: Changes not reflecting

**Symptoms:**
- Code changes don't appear
- .env changes don't work

**Solutions:**
1. For .env changes: MUST restart the dev server
2. For code changes: Should auto-reload (check console for errors)
3. Clear browser cache: Ctrl+Shift+R
4. Restart both services

## Startup Checklist

Before starting development, ensure:

- [ ] Backend .env file exists with GEMINI_API_KEY
- [ ] Backend .env has CORS_ORIGINS=http://localhost:3000
- [ ] Frontend .env file exists with REACT_APP_BACKEND_URL=http://localhost:3001
- [ ] Frontend .env does NOT have backend variables (GEMINI_API_KEY, DATABASE_URL)
- [ ] Python virtual environment is activated for backend
- [ ] All dependencies are installed (backend: pip install -r requirements.txt, frontend: npm install)

## Development Workflow

### Starting Both Services

**Terminal 1 (Backend):**
```bash
cd ai_app_backend
source venv/bin/activate
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

**Terminal 2 (Frontend):**
```bash
cd ai_app_frontend
npm start
```

### Making Changes

**Backend changes:**
- Edit Python files in `src/`
- Changes auto-reload with `--reload` flag
- Check backend terminal for errors

**Frontend changes:**
- Edit React files in `src/`
- Changes auto-reload (hot module replacement)
- Check browser console for errors

**Environment variable changes:**
- Edit .env file
- **MUST restart the server** (Ctrl+C, then restart command)

## API Documentation

Once the backend is running, access interactive API documentation:

- **Swagger UI**: http://localhost:3001/docs
- **ReDoc**: http://localhost:3001/redoc
- **OpenAPI JSON**: http://localhost:3001/openapi.json

## Database Setup (Optional)

The application works without a database (Q&A history is not persisted). To enable database:

1. Install and start PostgreSQL
2. Create database: `createdb ai_app_db`
3. Set DATABASE_URL in backend .env
4. Run initialization: `python database/init_db.py`
5. Restart backend

## Verification Commands

Run these to verify your setup:

```bash
# Check backend
cd ai_app_backend
./verify_setup.sh

# Check frontend
cd ai_app_frontend
./verify_setup.sh

# Manual checks
curl http://localhost:3001/health  # Backend health
curl http://localhost:3000          # Frontend (should return HTML)
```

## Environment Variable Reference

### Backend (ai_app_backend/.env)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| GEMINI_API_KEY | Yes | - | Google Gemini API key |
| DATABASE_URL | No | - | PostgreSQL connection string |
| CORS_ORIGINS | Yes | http://localhost:3000 | Allowed frontend origins |

### Frontend (ai_app_frontend/.env)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| REACT_APP_BACKEND_URL | Yes | http://localhost:3001 | Backend API URL |

## Production Deployment Notes

When deploying to production:

1. Update frontend .env: `REACT_APP_BACKEND_URL=https://your-backend-domain.com`
2. Update backend .env: `CORS_ORIGINS=https://your-frontend-domain.com`
3. Use production-grade server (Gunicorn for backend)
4. Set up proper database with backups
5. Use environment secrets management
6. Enable HTTPS/TLS

## Support

For issues:
1. Check this guide's troubleshooting section
2. Review backend README: `ai_app_backend/README.md`
3. Review frontend README: `ai_app_frontend/README.md`
4. Run verification scripts: `./verify_setup.sh`

## Summary

**Key Points to Remember:**
- Frontend: port 3000, Backend: port 3001
- Backend needs GEMINI_API_KEY to work
- Frontend .env should only have REACT_APP_BACKEND_URL
- Backend .env needs CORS_ORIGINS=http://localhost:3000
- Always restart dev servers after changing .env files
- Use verification scripts to check setup
