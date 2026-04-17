"""
Example client for Mini Notebook LLM Backend
Shows how to integrate the backend with frontend or other applications
"""
import asyncio
import httpx
from typing import Optional

class NotebookLLMClient:
    """Client for communicating with the Mini Notebook LLM Backend"""
    
    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 60.0):
        """
        Initialize the client
        
        Args:
            base_url: The base URL of the backend (default: http://localhost:8000)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
    
    async def health(self) -> dict:
        """Check if the backend is healthy"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/health")
            return response.json()
    
    async def chat(
        self,
        message: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> dict:
        """
        Send a chat message to the LLM
        
        Args:
            message: The message to send
            model: The model to use (optional, uses default if None)
            temperature: Creativity level (0.0-1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Dictionary with response, model, and tokens_used
        """
        payload = {
            "message": message,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        if model:
            payload["model"] = model
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat",
                json=payload
            )
            return response.json()
    
    async def complete_code(
        self,
        code_snippet: str,
        model: Optional[str] = None,
        temperature: float = 0.5,
        max_tokens: int = 500
    ) -> dict:
        """
        Get code completion suggestions
        
        Args:
            code_snippet: The code to complete
            model: The model to use
            temperature: Creativity level
            max_tokens: Maximum tokens
            
        Returns:
            Dictionary with completion and metadata
        """
        payload = {
            "message": code_snippet,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        if model:
            payload["model"] = model
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/code-complete",
                json=payload
            )
            return response.json()
    
    async def explain(
        self,
        topic: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> dict:
        """
        Get explanation for code or concepts
        
        Args:
            topic: What to explain
            model: The model to use
            temperature: Creativity level
            max_tokens: Maximum tokens
            
        Returns:
            Dictionary with explanation and metadata
        """
        payload = {
            "message": topic,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        if model:
            payload["model"] = model
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/explain",
                json=payload
            )
            return response.json()
    
    async def list_models(self) -> dict:
        """Get list of available models"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{self.base_url}/models")
            return response.json()


# Example usage
async def main():
    # Initialize client
    client = NotebookLLMClient()
    
    print("=" * 60)
    print("Mini Notebook LLM - Client Example")
    print("=" * 60)
    
    try:
        # Check health
        print("\n1. Checking backend health...")
        health = await client.health()
        print(f"   ✅ Backend Status: {health['status']}")
        print(f"   API Connected: {health['api_connected']}")
        
        # Chat example
        print("\n2. Chat Example...")
        print("   Question: What is machine learning?")
        chat_result = await client.chat(
            "What is machine learning in 2 sentences?",
            temperature=0.7,
            max_tokens=200
        )
        print(f"   Answer: {chat_result['response']}")
        print(f"   Tokens Used: {chat_result['tokens_used']}")
        
        # Code completion example
        print("\n3. Code Completion Example...")
        print("   Input: def hello_world(")
        complete_result = await client.complete_code(
            "def hello_world(",
            temperature=0.3,
            max_tokens=150
        )
        print(f"   Suggestion:\n{complete_result['completion']}")
        
        # Explanation example
        print("\n4. Code Explanation Example...")
        print("   Topic: What are decorators in Python?")
        explain_result = await client.explain(
            "What are decorators in Python and why are they useful?",
            temperature=0.7,
            max_tokens=300
        )
        print(f"   Explanation:\n{explain_result['response']}")
        
        # List models
        print("\n5. Available Models...")
        models_result = await client.list_models()
        data = models_result.get("data", [])
        print(f"   Total Models: {len(data)}")
        print("   Sample Models:")
        for model in data[:3]:
            print(f"     - {model.get('id', 'Unknown')}")
        
        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure the backend is running: python main.py")


# Alternative: Synchronous wrapper (if you prefer non-async code)
import time
from concurrent.futures import ThreadPoolExecutor

class SyncNotebookLLMClient:
    """Synchronous wrapper for the async client"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.client = NotebookLLMClient(base_url)
        self.executor = ThreadPoolExecutor(max_workers=1)
    
    def chat(self, message: str, **kwargs) -> dict:
        """Synchronous chat method"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.client.chat(message, **kwargs))
        finally:
            loop.close()
    
    def complete_code(self, code_snippet: str, **kwargs) -> dict:
        """Synchronous code completion method"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.client.complete_code(code_snippet, **kwargs))
        finally:
            loop.close()
    
    def explain(self, topic: str, **kwargs) -> dict:
        """Synchronous explanation method"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.client.explain(topic, **kwargs))
        finally:
            loop.close()


# Example of synchronous usage
def sync_example():
    """Example of using the synchronous client"""
    client = SyncNotebookLLMClient()
    
    # Simple chat
    result = client.chat("What is Python?")
    print(result['response'])
    
    # Code completion
    result = client.complete_code("x = [1, 2, 3]\ny = ")
    print(result['completion'])


if __name__ == "__main__":
    print("Running asynchronous examples...\n")
    asyncio.run(main())
    
    # Uncomment to run synchronous examples
    # print("\n\nRunning synchronous examples...\n")
    # sync_example()
