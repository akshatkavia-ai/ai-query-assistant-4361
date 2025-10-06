# AI Q&A Backend

FastAPI backend service for AI-powered question and answer application using Google's Gemini API.

## Features

- POST /ask endpoint for submitting questions and receiving AI-generated answers
- Persistent storage of Q&A history in PostgreSQL database
- Integration with Google Gemini API
- CORS support for frontend integration
- OpenAPI/Swagger documentation

## Environment Variables

Create a `.env` file in the backend root directory with the following variables:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql+psycopg2://user:password@host:port/database

# Optional
CORS_ORIGINS=*  # Comma-separated list of allowed origins, or * for all
```

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
python -m src.database.init_db
```

3. Run the server:
```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

## API Usage

### Ask a Question

**Endpoint:** `POST /ask`

**Request Body:**
```json
{
  "question": "What is the capital of France?"
}
```

**Response:**
```json
{
  "answer": "The capital of France is Paris.",
  "id": 1,
  "timestamp": "2024-01-15T10:30:00.123456Z"
}
```

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is artificial intelligence?"}'
```

**Example using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "What is artificial intelligence?"}
)
print(response.json())
```

### Health Check

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "Healthy",
  "service": "AI Q&A Backend"
}
```

## API Documentation

Once the server is running, access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad request (e.g., empty question)
- `500`: Internal server error
- `502`: Bad gateway (Gemini API failure)

## Timeout Configuration

The Gemini API call has a default timeout of 30 seconds. This can be adjusted in `src/services/gemini_client.py`.

## Database Schema

The `qa_history` table stores:
- `id`: Primary key
- `question`: User's question text
- `answer`: AI-generated answer
- `created_at`: Timestamp of creation

## Development

To regenerate the OpenAPI specification:
```bash
python -m src.api.generate_openapi
```

This will update `interfaces/openapi.json`.
