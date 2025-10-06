#!/bin/bash
# Setup Verification Script for AI Query Assistant Backend
# This script verifies that the backend is properly configured

echo "===================================================="
echo "AI Query Assistant Backend - Setup Verification"
echo "===================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check 1: .env file exists
echo "1. Checking .env file..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} .env file exists"
else
    echo -e "${RED}✗${NC} .env file not found"
    echo "   Run: cp .env.example .env"
    exit 1
fi

# Check 2: Environment variables are set
echo ""
echo "2. Checking environment variables..."
if grep -q "GEMINI_API_KEY=" .env && ! grep -q "GEMINI_API_KEY=your_gemini_api_key_here" .env; then
    echo -e "${GREEN}✓${NC} GEMINI_API_KEY is configured"
else
    echo -e "${YELLOW}⚠${NC} GEMINI_API_KEY needs to be set in .env"
fi

if grep -q "DATABASE_URL=" .env; then
    echo -e "${GREEN}✓${NC} DATABASE_URL is configured"
else
    echo -e "${YELLOW}⚠${NC} DATABASE_URL needs to be set in .env"
fi

if grep -q "CORS_ORIGINS=.*localhost:3000" .env; then
    echo -e "${GREEN}✓${NC} CORS_ORIGINS includes http://localhost:3000"
else
    echo -e "${RED}✗${NC} CORS_ORIGINS should include http://localhost:3000"
fi

# Check 3: Port 3001 availability
echo ""
echo "3. Checking port 3001..."
if netstat -tuln 2>/dev/null | grep -q ":3001"; then
    echo -e "${GREEN}✓${NC} Backend is running on port 3001"
    
    # Check 4: Health endpoint
    echo ""
    echo "4. Testing health endpoint..."
    HEALTH_RESPONSE=$(curl -s http://localhost:3001/health)
    if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
        echo -e "${GREEN}✓${NC} Health endpoint is responding"
        echo "   Response: $HEALTH_RESPONSE"
    else
        echo -e "${RED}✗${NC} Health endpoint not responding correctly"
    fi
    
    # Check 5: CORS configuration
    echo ""
    echo "5. Testing CORS configuration..."
    CORS_RESPONSE=$(curl -s -X OPTIONS http://localhost:3001/ask \
        -H "Origin: http://localhost:3000" \
        -H "Access-Control-Request-Method: POST" -i 2>&1 | grep "access-control-allow-origin")
    
    if echo "$CORS_RESPONSE" | grep -q "http://localhost:3000"; then
        echo -e "${GREEN}✓${NC} CORS allows requests from http://localhost:3000"
    else
        echo -e "${RED}✗${NC} CORS not properly configured for http://localhost:3000"
    fi
    
else
    echo -e "${YELLOW}⚠${NC} Backend is not running on port 3001"
    echo "   Start it with: uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload"
fi

# Check 6: Requirements installed
echo ""
echo "6. Checking Python dependencies..."
if python -c "import fastapi, uvicorn, sqlalchemy, psycopg2, pydantic, dotenv, google.generativeai" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} All required Python packages are installed"
else
    echo -e "${RED}✗${NC} Some required packages are missing"
    echo "   Run: pip install -r requirements.txt"
fi

echo ""
echo "===================================================="
echo "Verification Complete"
echo "===================================================="
