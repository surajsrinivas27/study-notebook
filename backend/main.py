import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Mini Notebook LLM API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "meta-llama/llama-2-7b-chat"

# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    model: str = DEFAULT_MODEL
    temperature: float = 0.7
    max_tokens: int = 1000

class ChatResponse(BaseModel):
    response: str
    model: str
    tokens_used: int

class CodeExecutionRequest(BaseModel):
    code: str
    language: str = "python"

class CodeExecutionResponse(BaseModel):
    output: str
    error: str = None

# Routes

@app.get("/")
async def root():
    return {"message": "Mini Notebook LLM API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "api_connected": API_KEY is not None}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to the LLM and get a response.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")
    
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Mini Notebook LLM"
            }
            
            payload = {
                "model": request.model,
                "messages": [
                    {"role": "user", "content": request.message}
                ],
                "temperature": request.temperature,
                "max_tokens": request.max_tokens,
            }
            
            response = await client.post(
                f"{API_BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"LLM API Error: {response.text}"
                )
            
            data = response.json()
            return ChatResponse(
                response=data["choices"][0]["message"]["content"],
                model=request.model,
                tokens_used=data.get("usage", {}).get("total_tokens", 0)
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling LLM: {str(e)}")

@app.post("/code-complete")
async def code_complete(request: ChatRequest):
    """
    Generate code completion suggestions.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")
    
    prompt = f"""You are a helpful code completion assistant. Complete the following code snippet:

{request.message}

Provide only the completion, no explanations."""
    
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Mini Notebook LLM"
            }
            
            payload = {
                "model": request.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": request.temperature,
                "max_tokens": request.max_tokens,
            }
            
            response = await client.post(
                f"{API_BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"LLM API Error: {response.text}"
                )
            
            data = response.json()
            return {
                "completion": data["choices"][0]["message"]["content"],
                "model": request.model,
                "tokens_used": data.get("usage", {}).get("total_tokens", 0)
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/explain")
async def explain(request: ChatRequest):
    """
    Generate explanations for code or concepts.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")
    
    prompt = f"""Please provide a clear and concise explanation:

{request.message}

Focus on clarity and practical understanding."""
    
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Mini Notebook LLM"
            }
            
            payload = {
                "model": request.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": request.temperature,
                "max_tokens": request.max_tokens,
            }
            
            response = await client.post(
                f"{API_BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"LLM API Error: {response.text}"
                )
            
            data = response.json()
            return ChatResponse(
                response=data["choices"][0]["message"]["content"],
                model=request.model,
                tokens_used=data.get("usage", {}).get("total_tokens", 0)
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/quiz")
async def generate_quiz(request: ChatRequest):
    """
    Generate quiz questions about a topic.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")
    
    topic = request.message.replace("quiz", "").strip() if "quiz" in request.message.lower() else request.message
    
    prompt = f"""Generate 3 interesting quiz questions about: {topic}

For each question provide:
1. Question text
2. Four multiple choice options (A, B, C, D)
3. Correct answer with explanation

Format clearly with labels."""
    
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Mini Notebook LLM"
            }
            
            payload = {
                "model": request.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000,
            }
            
            response = await client.post(
                f"{API_BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"LLM API Error: {response.text}"
                )
            
            data = response.json()
            return ChatResponse(
                response=data["choices"][0]["message"]["content"],
                model=request.model,
                tokens_used=data.get("usage", {}).get("total_tokens", 0)
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/models")
async def list_models():
    """
    List available models from OpenRouter.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")
    
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
            }
            
            response = await client.get(
                f"{API_BASE_URL}/models",
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to fetch models"
                )
            
            return response.json()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    # Support Render's PORT environment variable
    port = int(os.getenv("PORT", 8000))
    
    # Determine if we should enable reload (disable in production)
    debug_mode = os.getenv("DEBUG", "False").lower() == "true"
    reload_enabled = debug_mode
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port, 
        reload=reload_enabled,
        log_level="info"
    )
