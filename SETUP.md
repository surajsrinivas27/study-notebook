# Mini Notebook LLM Backend - Installation & Setup Guide

## Overview

This is a FastAPI-based backend for your Mini Notebook LLM application. It provides REST API endpoints for AI-powered features including code completion, explanations, and chat functionality using OpenRouter's LLM models.

## Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package manager (usually comes with Python)
- **API Key**: You already have this configured!

## Installation Steps

### Step 1: Install Dependencies

**On Windows:**
```bash
pip install -r requirements.txt
```

**On macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

### Step 2: Verify Installation

Check that FastAPI is installed:
```bash
python -m pip show fastapi
```

## Running the Server

### Option 1: Quick Start (Recommended for Windows)
Double-click `run.bat`

### Option 2: Quick Start (macOS/Linux)
```bash
chmod +x run.sh
./run.sh
```

### Option 3: Manual Start
```bash
python main.py
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## Testing the API

### Quick Test in Browser
Once the server is running:
1. Open your browser
2. Go to `http://localhost:8000/docs`
3. This opens the interactive API documentation
4. Try the `/health` endpoint first

### Automated Testing
In a new terminal/command prompt (with the server still running):
```bash
python test_api.py
```

This will run a comprehensive test suite of all endpoints.

### Manual Testing with cURL

**Windows (using PowerShell):**
```powershell
# Health check
curl -X GET "http://localhost:8000/health"

# Chat example
curl -X POST "http://localhost:8000/chat" `
  -H "Content-Type: application/json" `
  -d '{"message": "What is AI?"}'
```

**macOS/Linux:**
```bash
# Health check
curl http://localhost:8000/health

# Chat example
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is AI?"}'
```

### Testing in VS Code Rest Client

Create a file `test.http`:
```http
### Health Check
GET http://localhost:8000/health

### Chat
POST http://localhost:8000/chat
Content-Type: application/json

{
  "message": "What is Python?",
  "temperature": 0.7,
  "max_tokens": 500
}

### Code Completion
POST http://localhost:8000/code-complete
Content-Type: application/json

{
  "message": "def fibonacci(n",
  "temperature": 0.5,
  "max_tokens": 300
}

### Code Explanation
POST http://localhost:8000/explain
Content-Type: application/json

{
  "message": "What are decorators in Python?"
}

### List Models
GET http://localhost:8000/models
```

Install the "REST Client" extension, then click "Send Request" above each endpoint.

## Configuration

### Basic Configuration
Edit `.env` file if you need to change the API key:
```
OPENROUTER_API_KEY=your-key-here
```

### Server Configuration
Edit `main.py` to customize:
- **Line 16**: `DEFAULT_MODEL` - Change LLM model
- **Line 76**: `PORT` - Change from 8000 to another port
- **Line 76**: `HOST` - Change where the server listens

### Advanced Configuration
Edit `config.py` for:
- Request timeouts
- Max token limits
- CORS settings
- Logging levels
- Development vs. Production mode

## Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"
**Solution:**
```bash
pip install -r requirements.txt
```

### "Port 8000 already in use"
**Solution 1:** Stop the other process using port 8000
**Solution 2:** Change the port in `main.py` (line ~76):
```python
uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)  # Changed to 8001
```

### "Connection refused" when calling the API
**Solution:** Make sure the server is running:
```bash
python main.py
```

### "Authorization failed" or API key errors
**Solution:** Verify your `.env` file contains:
```
OPENROUTER_API_KEY=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
```

### Slow responses
This is normal as LLM inference takes time. You can:
- Reduce `max_tokens` in requests
- Use smaller models
- Increase the timeout value in `config.py`

## Architecture

```
┌─────────────────────────────────────────┐
│      Frontend (Notebook UI)             │
└──────────────────┬──────────────────────┘
                   │ HTTP Requests
                   ▼
┌─────────────────────────────────────────┐
│    FastAPI Backend (main.py)            │
│  ├─ /chat                              │
│  ├─ /code-complete                     │
│  ├─ /explain                           │
│  ├─ /models                            │
│  └─ /health                            │
└──────────────────┬──────────────────────┘
                   │ HTTPS API Calls
                   ▼
         ┌─────────────────────┐
         │  OpenRouter API     │
         │  (LLM Provider)     │
         └─────────────────────┘
```

## File Structure

```
mini notebook llm/
├── main.py              # Main FastAPI application
├── config.py            # Configuration management
├── utils.py             # Utility functions & classes
├── test_api.py          # API test suite
├── requirements.txt     # Python dependencies
├── .env                 # API key (keep secret!)
├── .gitignore           # Git ignore rules
├── run.bat              # Windows quick start
├── run.sh               # Linux/Mac quick start
├── README.md            # Feature documentation
└── SETUP.md             # This file
```

## Next Steps

1. **Test all endpoints** using `test_api.py`
2. **Integrate with frontend** - Use the API endpoints in your notebook UI
3. **Add database** - Store notebooks, history, and user data
4. **Deploy** - Move to production environment
5. **Add authentication** - Secure your API with user accounts

## Environment Setup for Different Scenarios

### Development Environment
```bash
# Install backend
pip install -r requirements.txt

# Run with hot reload
python main.py
```

### Production Setup
Create `.env`:
```
ENVIRONMENT=production
CORS_ORIGINS=https://yourdomain.com
DEBUG=False
```

Then deploy using:
```bash
# Using Gunicorn (recommended for production)
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## API Rate Limiting Notes

OpenRouter has rate limits. The default setup includes:
- Request timeout: 60 seconds
- Max tokens per request: 2000

For production, consider:
- Implementing request queuing
- Adding rate limiting middleware
- Caching responses
- Monitoring usage

## Security Tips

1. **Never commit `.env` file** - It contains your API key!
2. **Use environment variables** - Don't hardcode secrets
3. **Enable HTTPS** - In production, always use HTTPS
4. **Limit CORS origins** - Restrict who can call your API
5. **Add authentication** - Protect your endpoints

## Support & Documentation

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **OpenRouter Docs**: https://openrouter.ai/docs
- **API Interactive Docs**: `http://localhost:8000/docs` (when running)

## Performance Tips

- Reduce `max_tokens` for faster responses
- Use smaller models for real-time features
- Implement caching for common questions
- Consider implementing request batching

## Debugging

Enable debug logging by editing `.env`:
```
DEBUG=True
LOG_LEVEL=DEBUG
```

View the detailed logs in the terminal where you run `python main.py`.

---

**You're all set!** Your backend is ready to power your Mini Notebook LLM application. 🚀
