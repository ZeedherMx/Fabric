"""
Configuration management for the Chatbot Factory
"""
import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    """Application settings"""
    
    # API Keys
    groq_api_key: str = Field(..., env="GROQ_API_KEY")
    opik_api_key: Optional[str] = Field(None, env="OPIK_API_KEY")
    opik_workspace: Optional[str] = Field(None, env="OPIK_WORKSPACE")
    langfuse_secret_key: Optional[str] = Field(None, env="LANGFUSE_SECRET_KEY")
    langfuse_public_key: Optional[str] = Field(None, env="LANGFUSE_PUBLIC_KEY")
    langfuse_host: str = Field("https://cloud.langfuse.com", env="LANGFUSE_HOST")
    
    # Database
    database_url: str = Field("sqlite:///./chatbot_factory.db", env="DATABASE_URL")
    
    # LLM Configuration
    default_model: str = "llama-3.1-70b-versatile"
    temperature: float = 0.7
    max_tokens: int = 4096
    
    # Paths
    fabric_path: str = "./Fabric"
    output_path: str = "./Output_Chatbot"
    templates_path: str = "./Fabric/templates"
    
    # Docker
    docker_registry: str = Field("localhost:5000", env="DOCKER_REGISTRY")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
