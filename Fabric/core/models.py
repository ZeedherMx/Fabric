"""
Data models for the Chatbot Factory
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum

class ChatbotType(str, Enum):
    """Types of chatbots that can be generated"""
    CUSTOMER_SUPPORT = "customer_support"
    SALES_ASSISTANT = "sales_assistant"
    KNOWLEDGE_BASE = "knowledge_base"
    CREATIVE_ASSISTANT = "creative_assistant"
    TECHNICAL_SUPPORT = "technical_support"
    MULTI_AGENT_TEAM = "multi_agent_team"

class PersonalityTrait(str, Enum):
    """Personality traits for chatbots"""
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    CASUAL = "casual"
    FORMAL = "formal"
    HUMOROUS = "humorous"
    EMPATHETIC = "empathetic"
    DIRECT = "direct"

class IntegrationType(str, Enum):
    """Available integration types"""
    REST_API = "rest_api"
    DATABASE = "database"
    EMAIL = "email"
    SLACK = "slack"
    DISCORD = "discord"
    WEBHOOK = "webhook"
    FILE_SYSTEM = "file_system"
    SEARCH_ENGINE = "search_engine"

class AgentRole(str, Enum):
    """Roles for multi-agent systems"""
    COORDINATOR = "coordinator"
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    WRITER = "writer"
    REVIEWER = "reviewer"
    SPECIALIST = "specialist"

class ChatbotConfig(BaseModel):
    """Configuration for a chatbot to be generated"""
    
    # Basic Information
    name: str = Field(..., description="Name of the chatbot")
    description: str = Field(..., description="Purpose and description")
    chatbot_type: ChatbotType = Field(..., description="Type of chatbot")
    
    # Personality & Behavior
    personality_traits: List[PersonalityTrait] = Field(default=[], description="Personality traits")
    tone: str = Field("professional", description="Communication tone")
    language: str = Field("en", description="Primary language")
    
    # Knowledge & Context
    domain_expertise: List[str] = Field(default=[], description="Areas of expertise")
    knowledge_sources: List[str] = Field(default=[], description="Knowledge base sources")
    context_window: int = Field(4096, description="Context window size")
    
    # Capabilities
    enable_rag: bool = Field(True, description="Enable RAG capabilities")
    enable_function_calling: bool = Field(True, description="Enable function calling")
    enable_memory: bool = Field(True, description="Enable conversation memory")
    enable_web_search: bool = Field(False, description="Enable web search")
    
    # Integrations
    integrations: List[Dict[str, Any]] = Field(default=[], description="External integrations")
    api_endpoints: List[Dict[str, str]] = Field(default=[], description="API endpoints to integrate")
    
    # Multi-Agent Configuration
    is_multi_agent: bool = Field(False, description="Is this a multi-agent system")
    agents: List[Dict[str, Any]] = Field(default=[], description="Agent configurations")
    
    # UI Configuration
    ui_theme: str = Field("default", description="UI theme")
    custom_css: Optional[str] = Field(None, description="Custom CSS")
    logo_url: Optional[str] = Field(None, description="Logo URL")
    
    # Deployment
    enable_docker: bool = Field(True, description="Generate Docker configuration")
    port: int = Field(7860, description="Default port")
    
    # Advanced Settings
    max_conversation_length: int = Field(50, description="Max conversation turns")
    response_timeout: int = Field(30, description="Response timeout in seconds")
    rate_limit: Optional[int] = Field(None, description="Rate limit per minute")

class AgentConfig(BaseModel):
    """Configuration for individual agents in multi-agent systems"""
    name: str
    role: AgentRole
    description: str
    system_prompt: str
    tools: List[str] = Field(default=[])
    model: str = Field("llama-3.1-70b-versatile")
    temperature: float = Field(0.7)

class GenerationRequest(BaseModel):
    """Request model for chatbot generation"""
    config: ChatbotConfig
    output_name: str = Field(..., description="Name for the output folder")
    include_tests: bool = Field(True, description="Generate test files")
    include_docs: bool = Field(True, description="Generate documentation")

class GenerationResponse(BaseModel):
    """Response model for chatbot generation"""
    success: bool
    output_path: str
    message: str
    files_generated: List[str] = Field(default=[])
    docker_image: Optional[str] = Field(None)
    errors: List[str] = Field(default=[])
