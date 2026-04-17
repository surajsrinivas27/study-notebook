"""
Configuration module for Mini Notebook LLM Backend
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    
    # API Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
    
    # Default Model - can be changed to use different models
    DEFAULT_MODEL = "meta-llama/llama-2-7b-chat"
    
    # Alternative models you can try:
    # MODELS = {
    #     "llama2-7b": "meta-llama/llama-2-7b-chat",
    #     "llama2-13b": "meta-llama/llama-2-13b-chat",
    #     "openchat": "openchat/openchat-7b",
    #     "mistral": "mistralai/mistral-7b-instruct",
    # }
    
    # API Request Configuration
    REQUEST_TIMEOUT = 60.0
    CHAT_MAX_TOKENS = 2000
    CODE_MAX_TOKENS = 1500
    
    # Temperature range: 0.0 (deterministic) to 1.0 (creative)
    DEFAULT_TEMPERATURE = 0.7
    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    RELOAD = os.getenv("RELOAD", "True").lower() == "true"
    
    # CORS Configuration
    CORS_ORIGINS = ["*"]
    CORS_CREDENTIALS = True
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls):
        """Validate critical configuration"""
        if not cls.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY environment variable is not set")
        return True


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    RELOAD = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    RELOAD = False
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")


# Select configuration based on environment
environment = os.getenv("ENVIRONMENT", "development").lower()
if environment == "production":
    current_config = ProductionConfig()
else:
    current_config = DevelopmentConfig()

# Validate configuration
current_config.validate()
