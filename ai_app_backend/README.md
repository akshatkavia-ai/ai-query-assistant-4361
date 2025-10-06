# AI Query Assistant - Backend API

FastAPI backend service for the AI Query Assistant application. This service integrates with Google Gemini AI to answer user questions and persists Q&A history in a PostgreSQL database.

## Features

- **AI-Powered Q&A**: Leverages Google Gemini AI to generate intelligent answers
- **Persistent Storage**: Stores all Q&A pairs in PostgreSQL for history tracking
- **RESTful API**: Clean, documented API with automatic OpenAPI/Swagger docs
- **CORS Support**: Configurable cross-origin resource sharing
- **Health Checks**: Built-in health monitoring endpoints
- **Robust Error Handling**: Comprehensive error handling with user-friendly messages

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
└── .env.example           # Environment variable template
```

## Prerequisites

- **Python**: 3.9 or higher
- **PostgreSQL**: 12 or higher (running and accessible)
- **Google Gemini API Key**: Required for AI functionality
- **pip**: Python package installer

## Environment Variables

The backend requires the following environment variables:

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key for AI responses | `AIzaSyD...` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg2://user:pass@localhost:5432/dbname` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CORS_ORIGINS` | Comma-separated list of allowed origins | `http://localhost:3000` |

### Setting Up Environment Variables

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set your values:
   ```bash
   GEMINI_API_KEY=<your_actual_gemini_api_key>
   DATABASE_URL=postgresql+psycopg2://myuser:mypassword@localhost:5432/ai_assistant_db
   CORS_ORIGINS=http://localhost:3000
   ```

3. **Getting a Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Create a new API key
   - Copy the key to your `.env` file

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

### Step 3: Initialize Database

Make sure your PostgreSQL database is running and accessible, then run:

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
# Run with uvicorn (development)
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

# Or run directly with Python
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
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

The server will be available at `http://localhost:3001`

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

**Response Example:**
```json
{
  "answer": "The capital of France is Paris. It is located in the north-central part of the country and is known for its art, culture, and iconic landmarks such as the Eiffel Tower.",
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
| `500` | Internal Server Error | Database connection failed, unexpected error |
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

3. **Database Error (500):**
```json
{
  "detail": "Failed to save Q&A record to database"
}
```

## CORS Configuration

The backend is configured to accept requests from the frontend running on `http://localhost:3000` by default.

To allow additional origins, update the `CORS_ORIGINS` environment variable:

```bash
# Single origin
CORS_ORIGINS=http://localhost:3000

# Multiple origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://myapp.com
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

## Troubleshooting

### Issue 1: Database Connection Failed

**Symptoms:**
- Error: "Database connection failed"
- Server starts but shows database warnings
- 500 errors when making requests

**Solutions:**

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
   postgresql+psycopg2://postgres:mypassword@localhost:5432/ai_assistant_db
   ```

3. **Test database connection:**
   ```bash
   # Using psql
   psql -h localhost -p 5432 -U postgres -d ai_assistant_db
   ```

4. **Check database credentials:**
   - Username and password are correct
   - Database exists
   - User has necessary permissions

5. **Run init script again:**
   ```bash
   python database/init_db.py
   ```

### Issue 2: GEMINI_API_KEY Not Configured

**Symptoms:**
- 503 Service Unavailable errors
- Error: "AI service is not available"
- `/health` shows `gemini: "unavailable"`

**Solutions:**

1. **Verify API key is set:**
   ```bash
   # Check .env file
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

### Issue 3: CORS Errors from Frontend

**Symptoms:**
- Browser console shows CORS errors
- Network requests fail with CORS policy errors
- Error: "Access to fetch has been blocked by CORS policy"

**Solutions:**

1. **Verify CORS_ORIGINS includes frontend URL:**
   ```bash
   # In .env file:
   CORS_ORIGINS=http://localhost:3000
   ```

2. **Check frontend is running on correct port:**
   - Frontend should be on port 3000
   - Backend should be on port 3001

3. **Restart backend after changing CORS settings**

4. **For production, add production URL:**
   ```bash
   CORS_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
   ```

### Issue 4: Port Already in Use

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

2. **Use a different port:**
   ```bash
   uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   
   Remember to update `REACT_APP_BACKEND_URL` in frontend!

### Issue 5: Module Import Errors

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

## Startup Order

For the full application stack to work correctly, start services in this order:

1. **Database (PostgreSQL)**: Must be running first
2. **Backend API**: Starts and connects to database
3. **Frontend**: Connects to backend API

```bash
# 1. Start PostgreSQL (if not already running)
sudo systemctl start postgresql

# 2. Initialize database (first time only)
cd ai_app_backend
python database/init_db.py

# 3. Start backend server
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

# 4. In another terminal, start frontend
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

The OpenAPI specification is automatically available at `/openapi.json` when the server is running. To save it to a file:

```bash
python src/api/generate_openapi.py
```

This will create/update `interfaces/openapi.json`.

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
GEMINI_API_KEY=<your_production_key>
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

**Note**: This backend is designed to work with the AI Query Assistant frontend. Ensure both services are running for full functionality.
