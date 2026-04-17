# Mini Notebook LLM Backend

A FastAPI backend for AI-powered notebook functionality with LLM integration via OpenRouter.

## Features

- **Chat API**: Send messages to various LLM models
- **Code Completion**: Get intelligent code suggestions
- **Code Explanation**: Get explanations for code snippets
- **Model Listing**: Browse available LLM models
- **CORS Support**: Works with frontend applications
- **Async Support**: High-performance asynchronous operations

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

The `.env` file is pre-configured with your API key:
```
OPENROUTER_API_KEY=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
```

### 3. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API docs available at: `http://localhost:8000/docs`

### Endpoints

#### Health Check
```
GET /health
```
Check if the API is running and connected.

#### Chat
```
POST /chat
```
Send a message to an LLM model.

Request body:
```json
{
  "message": "Your message here",
  "model": "meta-llama/llama-2-7b-chat",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

#### Code Completion
```
POST /code-complete
```
Get code completion suggestions.

Request body:
```json
{
  "message": "def hello",
  "model": "meta-llama/llama-2-7b-chat",
  "temperature": 0.7,
  "max_tokens": 500
}
```

#### Code Explanation
```
POST /explain
```
Get explanations for code or concepts.

Request body:
```json
{
  "message": "What does async/await do in Python?",
  "model": "meta-llama/llama-2-7b-chat",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

#### List Models
```
GET /models
```
Get a list of available models from OpenRouter.

## Example Usage

### Using cURL

```bash
# Chat
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Python?",
    "model": "meta-llama/llama-2-7b-chat",
    "temperature": 0.7,
    "max_tokens": 500
  }'

# Code Completion
curl -X POST "http://localhost:8000/code-complete" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "def fibonacci(",
    "model": "meta-llama/llama-2-7b-chat"
  }'

# Code Explanation
curl -X POST "http://localhost:8000/explain" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain decorators in Python"
  }'
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Chat
response = requests.post(f"{BASE_URL}/chat", json={
    "message": "What is FastAPI?",
    "temperature": 0.7,
    "max_tokens": 500
})
print(response.json())

# Code Completion
response = requests.post(f"{BASE_URL}/code-complete", json={
    "message": "async def fetch_data"
})
print(response.json())
```

## Configuration

Edit `main.py` to customize:
- `DEFAULT_MODEL`: Change the default LLM model
- `API_BASE_URL`: Change API endpoint (default: OpenRouter)
- Host and port in the `if __name__ == "__main__"` section

## Available Models on OpenRouter

Popular models include:
- `meta-llama/llama-2-7b-chat`
- `meta-llama/llama-2-13b-chat`
- `openchat/openchat-7b`
- `mistralai/mistral-7b-instruct`
- And many more available via the `/models` endpoint

## Project Structure

```
mini notebook llm/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (API key)
└── README.md           # This file
```

## Troubleshooting

### API Key Error
Ensure your `.env` file contains a valid `OPENROUTER_API_KEY`.

### Connection Refused
Make sure the server is running:
```bash
python main.py
```

### CORS Issues
The API includes CORS middleware to accept requests from any origin. If you need to restrict this, edit the `CORSMiddleware` configuration in `main.py`.

## Next Steps

1. **Frontend Integration**: Connect this backend to your notebook UI
2. **Database**: Add persistent storage for notebook cells and history
3. **Authentication**: Implement user authentication if needed
4. **Rate Limiting**: Add rate limiting to control API usage
5. **Logging**: Add comprehensive logging for debugging

## License

MIT
