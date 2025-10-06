# AI Query Assistant - Backend API

FastAPI backend service for the AI Query Assistant application. This service integrates with Google Gemini AI to answer user questions and persists Q&A history in a PostgreSQL database.

## Local Development Setup

**Important: For local development, use these exact ports:**
- **Backend**: http://localhost:3001 (FastAPI server, binds to 0.0.0.0:3001)
- **Frontend**: http://localhost:3000 (React dev server)

## Features

- **AI-Powered Q&A**: Leverages Google Gemini AI to generate intelligent answers
- **Persistent Storage**: Stores all Q&A pairs in PostgreSQL for history tracking
- **RESTful API**: Clean, documented API with automatic OpenAPI/Swagger docs
- **CORS Support**: Configurable cross-origin resource sharing
- **Health Checks**: Built-in health monitoring endpoints
- **Robust Error Handling**: Comprehensive error handling with user-friendly messages
- **Graceful Degradation**: Backend starts even if database or Gemini API are not available

## Architecture

```
ai_app_backend/
├── database/
│   ├── init_db.py          # Database initialization script
│   └── schema.sql          # Database schema definition
├── src/
│   ├── api/
│   │   ├── main.py         # FastAPI application entry point
│   │   └── routes/
│   │       └── ask.py      # /ask endpoint implementation
│   ├── database/
│   │   ├── connection.py   # Database connection and session management
│   │   └── models.py       # SQLAlchemy ORM models
│   ├── services/
│   │   └── gemini_service.py  # Gemini AI integration
│   └── schemas.py          # Pydantic request/response schemas
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variable template
└── start_server.sh        # Server startup script
```

## Prerequisites

- **Python**: 3.9 or higher
- **PostgreSQL**: 12 or higher (optional, backend starts without it)
- **Google Gemini API Key**: Required for AI functionality
- **pip**: Python package installer

## Environment Variables

The backend requires the following environment variables:

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key for AI responses | `AIzaSyD...` |

### Optional Variables (Backend starts without these)

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | None (optional) |
| `CORS_ORIGINS` | Comma-separated list of allowed origins | `http://localhost:3000` |

**Important Notes:**
- Backend will start and run even if `DATABASE_URL` is not set or database is unavailable
- Backend will start even if `GEMINI_API_KEY` is not set (but /ask endpoint will return 503)
- For local development with React frontend, CORS_ORIGINS must include `http://localhost:3000`

### Setting Up Environment Variables

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set your values:
   ```bash
   # Required for AI functionality
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   
   # Optional - Database (backend starts without this)
   DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/ai_app_db
   
   # Required for frontend communication
   CORS_ORIGINS=http://localhost:3000
   ```

3. **Getting a Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Create a new API key
   - Copy the key to your `.env` file

**Sanity Check:** Backend `.env` should NOT contain frontend-specific variables like:
- ❌ `REACT_APP_BACKEND_URL` (belongs in frontend)
- ❌ Any variables starting with `REACT_APP_` (belongs in frontend)

## Installation & Setup

### Step 1: Install Dependencies

```bash
# Navigate to backend directory
cd ai_app_backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your actual values
nano .env  # or use your preferred editor
```

**Minimal configuration for local development:**
```bash
GEMINI_API_KEY=your_actual_key_here
CORS_ORIGINS=http://localhost:3000
```

### Step 3: Initialize Database (Optional)

**Note:** This step is optional. The backend will start even if the database is not available.

If you want to persist Q&A history, make sure PostgreSQL is running, then:

```bash
# Run database initialization script
python database/init_db.py
```

This script will:
- Connect to your PostgreSQL database
- Create the `qa_history` table if it doesn't exist
- Create necessary indexes
- Verify the schema is properly set up

**Expected Output:**
```
============================================================
Database Initialization Script
============================================================
Connecting to database...
Executing schema.sql...
✓ Database schema initialized successfully!
============================================================
Initialization complete!
```

### Step 4: Start the Server

```bash
# Start server on port 3001, binding to 0.0.0.0
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

# Or use the startup script
./start_server.sh
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['/path/to/ai_app_backend']
INFO:     Uvicorn running on http://0.0.0.0:3001 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
============================================================
Starting AI Query Assistant Backend
============================================================
INFO:     Configuring CORS with origins: ['http://localhost:3000']
INFO:     Attempting database connection (attempt 1/5)...
INFO:     ✓ Database connection established successfully!
INFO:     Application startup complete
============================================================
INFO:     Application startup complete.
```

**Note:** If database is not available, you'll see:
```
⚠ Starting application without database connection
```
The server will still start and run, but Q&A history won't be persisted.

**Server Binding:** The server binds to `0.0.0.0:3001`, making it accessible from:
- Localhost: http://localhost:3001
- Any network interface on port 3001

## API Documentation

### Interactive API Docs

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:3001/docs
- **ReDoc**: http://localhost:3001/redoc
- **OpenAPI JSON**: http://localhost:3001/openapi.json

### Endpoints

#### 1. Health Check

**GET /**

Simple health check endpoint.

```bash
curl http://localhost:3001/
```

**Response:**
```json
{
  "status": "healthy",
  "message": "AI Query Assistant API is running",
  "version": "1.0.0"
}
```

#### 2. Detailed Health Check

**GET /health**

Detailed health check with service status.

```bash
curl http://localhost:3001/health
```

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "api": "operational",
    "gemini": "available"
  },
  "version": "1.0.0"
}
```

#### 3. Ask Question (Main Endpoint)

**POST /ask**

Submit a question to the AI assistant and receive an answer.

**Request Body:**
```json
{
  "question": "What is artificial intelligence?"
}
```

**Response (200 OK):**
```json
{
  "answer": "Artificial intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems. These processes include learning, reasoning, and self-correction...",
  "id": 42,
  "created_at": "2024-01-15T10:30:00.123456+00:00"
}
```

**Example curl command:**
```bash
curl -X POST http://localhost:3001/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the capital of France?"}'
```

**Testing from frontend (port 3000):**
```bash
curl -X POST http://localhost:3001/ask \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3000" \
  -d '{"question": "Hello, how are you?"}'
```

**Expected Response:**
```json
{
  "answer": "Hello! I'm doing well, thank you for asking...",
  "id": 1,
  "created_at": "2024-01-15T14:23:45.678901+00:00"
}
```

**Validation Rules:**
- Question must be between 1 and 5000 characters
- Question cannot be empty or only whitespace
- Question is required

**Error Responses:**

| Status Code | Description | Example |
|-------------|-------------|---------|
| `400` | Bad Request - Invalid input | Empty question, validation failure |
| `500` | Internal Server Error | Unexpected error |
| `503` | Service Unavailable | Gemini API not configured, quota exceeded |

**Error Response Format:**
```json
{
  "detail": "AI service is not available. Please ensure GEMINI_API_KEY is configured."
}
```

**Common Error Scenarios:**

1. **Missing API Key (503):**
```json
{
  "detail": "AI service is not available. Please ensure GEMINI_API_KEY is configured."
}
```

2. **Invalid Question (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "question"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

## CORS Configuration

**For local development with React frontend on port 3000:**

Backend `.env` must include:
```bash
CORS_ORIGINS=http://localhost:3000
```

**Sanity Check Checklist:**
- ✅ Backend `.env` contains: `CORS_ORIGINS=http://localhost:3000`
- ✅ Frontend runs on: http://localhost:3000
- ✅ Backend runs on: http://localhost:3001
- ✅ Backend binds to: 0.0.0.0:3001

**For multiple origins (e.g., local + production):**
```bash
CORS_ORIGINS=http://localhost:3000,https://myapp.com
```

**Important for Production:**
- Always specify exact origins in production
- Avoid using wildcards (`*`) in production environments
- Include your deployed frontend URL

## Database Schema

The application uses a single table to store Q&A history:

```sql
CREATE TABLE qa_history (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_qa_history_created_at ON qa_history(created_at DESC);
```

**Note:** If database is not available, the backend still runs but doesn't persist Q&A history.

## Troubleshooting

### Issue 1: Port 3001 Already in Use

**Symptoms:**
- Error: "Address already in use"
- Server fails to start

**Solutions:**

1. **Find process using port 3001:**
   ```bash
   # Linux/Mac
   lsof -i :3001
   
   # Kill the process
   kill -9 <PID>
   ```

2. **Or use a different port (not recommended for local dev):**
   ```bash
   uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   
   **Note:** If you change backend port, update frontend `REACT_APP_BACKEND_URL`!

### Issue 2: CORS Errors from Frontend

**Symptoms:**
- Browser console shows CORS errors
- Network requests from frontend fail
- Error: "Access to fetch has been blocked by CORS policy"

**Solutions:**

1. **Verify CORS_ORIGINS includes frontend URL:**
   ```bash
   cat .env | grep CORS_ORIGINS
   # Should show: CORS_ORIGINS=http://localhost:3000
   ```

2. **Verify frontend is on port 3000:**
   ```bash
   # Frontend should be at http://localhost:3000
   curl http://localhost:3000
   ```

3. **Restart backend after changing CORS settings:**
   ```bash
   # Stop server (Ctrl+C), then:
   uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
   ```

4. **Test CORS preflight:**
   ```bash
   curl -X OPTIONS http://localhost:3001/ask \
     -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -v
   ```

### Issue 3: GEMINI_API_KEY Not Configured

**Symptoms:**
- 503 Service Unavailable errors on /ask endpoint
- Error: "AI service is not available"
- `/health` shows `gemini: "unavailable"`

**Solutions:**

1. **Verify API key is set:**
   ```bash
   cat .env | grep GEMINI_API_KEY
   ```

2. **Get a valid API key:**
   - Visit https://makersuite.google.com/app/apikey
   - Create a new key
   - Add to `.env` file

3. **Restart the server** after updating `.env`

4. **Check for whitespace:**
   ```bash
   # No spaces around the = sign
   GEMINI_API_KEY=AIzaSyD...
   ```

### Issue 4: Database Connection Failed

**Symptoms:**
- Warning: "Starting application without database connection"
- Q&A pairs not being saved

**Note:** This is not a critical error! The backend runs without database.

**Solutions (if you want to persist history):**

1. **Verify PostgreSQL is running:**
   ```bash
   # Check if PostgreSQL is running
   sudo systemctl status postgresql
   # Or
   pg_isready
   ```

2. **Check DATABASE_URL format:**
   ```bash
   # Correct format:
   postgresql+psycopg2://username:password@host:port/database_name
   
   # Example:
   postgresql+psycopg2://postgres:password@localhost:5432/ai_app_db
   ```

3. **Test database connection:**
   ```bash
   # Using psql
   psql -h localhost -p 5432 -U postgres -d ai_app_db
   ```

4. **Run init script:**
   ```bash
   python database/init_db.py
   ```

### Issue 5: Frontend Can't Connect to Backend

**Symptoms:**
- Frontend shows "Cannot connect to backend"
- Network errors in browser console
- curl works but browser doesn't

**Solutions:**

1. **Verify backend is running on 0.0.0.0:3001:**
   ```bash
   # Backend should bind to 0.0.0.0, not 127.0.0.1
   uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
   ```

2. **Check backend health:**
   ```bash
   curl http://localhost:3001/health
   ```

3. **Verify CORS configuration:**
   ```bash
   cat .env | grep CORS_ORIGINS
   # Should be: CORS_ORIGINS=http://localhost:3000
   ```

4. **Check frontend .env:**
   ```bash
   # In frontend directory:
   cat .env
   # Should be: REACT_APP_BACKEND_URL=http://localhost:3001
   ```

5. **Restart both services:**
   ```bash
   # Backend (Ctrl+C, then):
   uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
   
   # Frontend (Ctrl+C, then):
   npm start
   ```

### Issue 6: Module Import Errors

**Symptoms:**
- ImportError or ModuleNotFoundError
- Server fails to start

**Solutions:**

1. **Reinstall dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure virtual environment is activated:**
   ```bash
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Check Python version:**
   ```bash
   python --version  # Should be 3.9+
   ```

## Local Development - Sanity Check

**Before starting development, verify this configuration:**

✅ **Backend Configuration:**
- [ ] Backend `.env` contains: `GEMINI_API_KEY=your_key_here`
- [ ] Backend `.env` contains: `CORS_ORIGINS=http://localhost:3000`
- [ ] Backend `.env` optionally contains: `DATABASE_URL=...` (not required)
- [ ] Backend does NOT contain: `REACT_APP_*` variables
- [ ] Backend starts with: `uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload`
- [ ] Backend accessible at: http://localhost:3001/health

✅ **Frontend Configuration:**
- [ ] Frontend `.env` contains ONLY: `REACT_APP_BACKEND_URL=http://localhost:3001`
- [ ] Frontend running on: http://localhost:3000
- [ ] Frontend can reach backend: Check browser console

✅ **After Changes:**
- [ ] Restart backend after changing backend `.env`
- [ ] Restart frontend after changing frontend `.env`
- [ ] Hard refresh browser (Ctrl+Shift+R)

## Startup Order

For the full application stack to work correctly:

1. **Database (PostgreSQL)**: Optional, backend starts without it
2. **Backend API**: Start on port 3001
3. **Frontend**: Start on port 3000

```bash
# Terminal 1: Backend (always bind to 0.0.0.0)
cd ai_app_backend
source venv/bin/activate
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

# Terminal 2: Frontend
cd ai_app_frontend
npm start
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_routes.py
```

### Code Quality

```bash
# Run linter
flake8 src/

# Format code
black src/
```

### Generating OpenAPI Spec

The OpenAPI specification is automatically available at `/openapi.json` when the server is running.

## Production Deployment

### Environment Configuration

1. Set production environment variables
2. Use strong database credentials
3. Configure appropriate CORS origins
4. Enable HTTPS/TLS
5. Set up proper logging

### Recommended Settings

```bash
# Production .env
GEMINI_API_KEY=your_production_key
DATABASE_URL=postgresql+psycopg2://user:secure_password@db_host:5432/prod_db
CORS_ORIGINS=https://your-production-frontend.com
```

### Running with Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with workers
gunicorn src.api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:3001
```

## Support & Resources

- **API Documentation**: http://localhost:3001/docs
- **Google Gemini AI**: https://ai.google.dev/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/

## License

[Your License Here]

## Version

**Current Version**: 1.0.0

---

**Note**: This backend is designed to work with the AI Query Assistant frontend running on port 3000. Ensure both services are configured correctly for local development.
