# Quick Reference Guide

## Starting the Backend

### Windows
```bash
# Option 1: Double-click
run.bat

# Option 2: Command line
python main.py
```

### macOS/Linux
```bash
./run.sh
# or
python main.py
```

## API Endpoints Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/chat` | POST | Chat with LLM |
| `/code-complete` | POST | Code suggestions |
| `/explain` | POST | Get explanations |
| `/models` | GET | List available models |
| `/docs` | GET | Interactive API docs |

## Example Requests

### Chat
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! Who are you?", "max_tokens": 200}'
```

### Code Completion
```bash
curl -X POST "http://localhost:8000/code-complete" \
  -H "Content-Type: application/json" \
  -d '{"message": "def factorial(n", "max_tokens": 300}'
```

### Code Explanation
```bash
curl -X POST "http://localhost:8000/explain" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is recursion?", "max_tokens": 500}'
```

## Testing

### Run Full Test Suite
```bash
python test_api.py
```

### Test in Browser
1. Start backend: `python main.py`
2. Open: `http://localhost:8000/docs`
3. Click on endpoints to test

## Configuration

### Change Port
Edit `main.py`, find the `if __name__ == "__main__":` section:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change 8000 to your port
```

### Change Default Model
Edit `config.py`:
```python
DEFAULT_MODEL = "meta-llama/llama-2-7b-chat"  # Change this
```

### Change API Key
Edit `.env`:
```
OPENROUTER_API_KEY=your-new-key-here
```

## Using in Python

### Async Code
```python
import asyncio
from client_example import NotebookLLMClient

async def main():
    client = NotebookLLMClient()
    result = await client.chat("What is AI?")
    print(result['response'])

asyncio.run(main())
```

### Sync Code
```python
from client_example import SyncNotebookLLMClient

client = SyncNotebookLLMClient()
result = client.chat("What is AI?")
print(result['response'])
```

## Using with Requests Library

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "Hello!"}
)
print(response.json()['response'])
```

## Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Port already in use | Change port in `main.py` |
| API key error | Check `.env` file |
| Connection refused | Make sure `python main.py` is running |
| Slow responses | Reduce `max_tokens` or use smaller model |

## File Reference

| File | Purpose |
|------|---------|
| `main.py` | Main FastAPI application |
| `config.py` | Configuration settings |
| `utils.py` | Utility classes and functions |
| `client_example.py` | Example client implementation |
| `test_api.py` | Automated API tests |
| `requirements.txt` | Python dependencies |
| `.env` | API key (keep secret) |
| `README.md` | Full documentation |
| `SETUP.md` | Installation guide |
| `run.bat` | Windows quick start |
| `run.sh` | Linux/Mac quick start |

## Directory Structure
```
mini notebook llm/
├── main.py                 # Core application
├── config.py               # Settings
├── utils.py                # Helper classes
├── client_example.py       # Client examples
├── test_api.py            # Test suite
├── requirements.txt        # Dependencies
├── .env                   # API key (SECRET)
├── README.md              # Documentation
├── SETUP.md               # Installation
├── QUICKREF.md            # This file
├── run.bat                # Windows starter
├── run.sh                 # Linux/Mac starter
└── .gitignore             # Git ignore rules
```

## Next Steps

1. ✅ Backend is installed and configured
2. 🚀 Start the backend: `python main.py`
3. 🧪 Run tests: `python test_api.py`
4. 📚 Read API docs: `http://localhost:8000/docs`
5. 🔗 Integrate with your frontend
6. 🚀 Deploy to production

## Support

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **OpenRouter Documentation**: https://openrouter.ai/docs
- **Interactive API Docs**: `http://localhost:8000/docs` (when running)

---

Ready to build! 🚀
