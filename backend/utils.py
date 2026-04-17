"""
Utility functions for the Mini Notebook LLM backend
"""
import asyncio
from typing import List, Dict, Any
import httpx

class NotebookCell:
    """Represents a notebook cell with code and metadata"""
    
    def __init__(self, cell_id: str, cell_type: str, source: str, metadata: Dict[str, Any] = None):
        self.cell_id = cell_id
        self.cell_type = cell_type  # 'code' or 'markdown'
        self.source = source
        self.metadata = metadata or {}
        self.outputs = []
    
    def to_dict(self):
        return {
            "cell_id": self.cell_id,
            "cell_type": self.cell_type,
            "source": self.source,
            "metadata": self.metadata,
            "outputs": self.outputs
        }


class NotebookManager:
    """Manages notebook operations"""
    
    def __init__(self):
        self.notebooks: Dict[str, List[NotebookCell]] = {}
    
    def create_notebook(self, notebook_id: str):
        """Create a new notebook"""
        self.notebooks[notebook_id] = []
    
    def add_cell(self, notebook_id: str, cell_id: str, cell_type: str, source: str):
        """Add a cell to a notebook"""
        if notebook_id not in self.notebooks:
            self.create_notebook(notebook_id)
        
        cell = NotebookCell(cell_id, cell_type, source)
        self.notebooks[notebook_id].append(cell)
        return cell
    
    def get_notebook(self, notebook_id: str):
        """Get all cells in a notebook"""
        return self.notebooks.get(notebook_id, [])
    
    def delete_cell(self, notebook_id: str, cell_id: str):
        """Delete a cell from a notebook"""
        if notebook_id in self.notebooks:
            self.notebooks[notebook_id] = [
                cell for cell in self.notebooks[notebook_id]
                if cell.cell_id != cell_id
            ]


class LLMHelper:
    """Helper class for LLM operations"""
    
    @staticmethod
    def create_code_prompt(code_snippet: str, task: str = "complete") -> str:
        """Create a prompt for code-related tasks"""
        prompts = {
            "complete": f"Complete this code:\n\n{code_snippet}\n\nProvide only the completion.",
            "explain": f"Explain this code:\n\n{code_snippet}\n\nProvide a clear explanation.",
            "fix": f"Fix any issues in this code:\n\n{code_snippet}\n\nProvide the corrected code.",
            "optimize": f"Optimize this code:\n\n{code_snippet}\n\nProvide optimized version.",
        }
        return prompts.get(task, prompts["complete"])
    
    @staticmethod
    def create_system_prompt(role: str = "assistant") -> str:
        """Create a system prompt based on role"""
        roles = {
            "assistant": "You are a helpful AI assistant.",
            "coder": "You are an expert programmer. Provide code solutions with explanations.",
            "teacher": "You are an educational assistant. Explain concepts clearly and provide examples.",
            "debugger": "You are a debugging expert. Identify and fix code issues.",
        }
        return roles.get(role, roles["assistant"])
    
    @staticmethod
    def parse_code_block(response: str) -> str:
        """Extract code from markdown code blocks"""
        import re
        pattern = r"```(?:python|javascript|java|cpp|csharp|ruby|go|rust|php)?\n(.*?)```"
        match = re.search(pattern, response, re.DOTALL)
        if match:
            return match.group(1).strip()
        return response


# Example usage functions
async def example_chat_usage(api_key: str):
    """Example of making a chat request"""
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": "meta-llama/llama-2-7b-chat",
            "messages": [
                {"role": "user", "content": "What is Python?"}
            ],
            "temperature": 0.7,
            "max_tokens": 500,
        }
        
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers
        )
        
        return response.json()


# Initialize notebook manager instance
notebook_manager = NotebookManager()
llm_helper = LLMHelper()
