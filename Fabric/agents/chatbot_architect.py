"""
Chatbot Architect Agent - Designs the overall chatbot architecture
"""
from typing import Dict, Any, List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph import StateGraph, END
from ..core.models import ChatbotConfig, AgentConfig, AgentRole
from ..core.config import settings
from ..core.observability import observability

class ChatbotArchitect:
    """Agent responsible for designing chatbot architecture"""
    
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=settings.groq_api_key,
            model_name=settings.default_model,
            temperature=0.3  # Lower temperature for more consistent architecture decisions
        )
    
    @observability.track_llm_call
    def design_architecture(self, config: ChatbotConfig) -> Dict[str, Any]:
        """Design the overall architecture for the chatbot"""
        
        system_prompt = """You are an expert chatbot architect. Your job is to design the optimal architecture for a chatbot based on the given requirements.

Consider:
1. Single-agent vs multi-agent approach
2. Required tools and integrations
3. Data flow and processing pipeline
4. Scalability and performance requirements
5. Security considerations

Provide a detailed architecture plan in JSON format."""

        user_prompt = f"""
Design architecture for a chatbot with these requirements:

Name: {config.name}
Type: {config.chatbot_type}
Description: {config.description}
Personality: {config.personality_traits}
Domain Expertise: {config.domain_expertise}
Capabilities:
- RAG: {config.enable_rag}
- Function Calling: {config.enable_function_calling}
- Memory: {config.enable_memory}
- Web Search: {config.enable_web_search}
Integrations: {config.integrations}
Multi-agent: {config.is_multi_agent}

Provide architecture recommendations including:
1. Agent structure (single or multi-agent)
2. Required tools and capabilities
3. Data storage requirements
4. API integrations needed
5. Recommended tech stack components
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Parse and structure the response
        architecture = self._parse_architecture_response(response.content, config)
        
        return architecture
    
    def _parse_architecture_response(self, response: str, config: ChatbotConfig) -> Dict[str, Any]:
        """Parse the LLM response and structure it"""
        
        # Basic architecture structure
        architecture = {
            "type": "multi_agent" if config.is_multi_agent else "single_agent",
            "agents": [],
            "tools": [],
            "integrations": [],
            "data_stores": [],
            "api_endpoints": [],
            "tech_stack": {
                "framework": "langgraph",
                "llm": "groq",
                "ui": "gradio",
                "api": "fastapi",
                "observability": "opik"
            }
        }
        
        # Determine agents based on config
        if config.is_multi_agent:
            architecture["agents"] = self._design_multi_agent_system(config)
        else:
            architecture["agents"] = [self._design_single_agent(config)]
        
        # Add tools based on capabilities
        if config.enable_rag:
            architecture["tools"].append("vector_search")
            architecture["data_stores"].append("vector_db")
        
        if config.enable_function_calling:
            architecture["tools"].append("function_calling")
        
        if config.enable_memory:
            architecture["data_stores"].append("conversation_memory")
        
        if config.enable_web_search:
            architecture["tools"].append("web_search")
        
        # Add integrations
        for integration in config.integrations:
            architecture["integrations"].append(integration)
        
        return architecture
    
    def _design_single_agent(self, config: ChatbotConfig) -> Dict[str, Any]:
        """Design a single agent configuration"""
        return {
            "name": f"{config.name}_agent",
            "role": "primary",
            "description": config.description,
            "capabilities": [
                "conversation",
                "task_execution",
                "information_retrieval" if config.enable_rag else None,
                "function_calling" if config.enable_function_calling else None
            ],
            "tools": self._get_tools_for_config(config),
            "model": settings.default_model,
            "temperature": settings.temperature
        }
    
    def _design_multi_agent_system(self, config: ChatbotConfig) -> List[Dict[str, Any]]:
        """Design a multi-agent system configuration"""
        agents = []
        
        # Coordinator agent (always present in multi-agent systems)
        agents.append({
            "name": "coordinator",
            "role": "coordinator",
            "description": "Coordinates tasks between specialized agents",
            "capabilities": ["task_routing", "response_synthesis"],
            "tools": ["agent_communication"],
            "model": settings.default_model,
            "temperature": 0.3
        })
        
        # Add specialized agents based on chatbot type
        if config.chatbot_type == "customer_support":
            agents.extend([
                {
                    "name": "support_specialist",
                    "role": "specialist",
                    "description": "Handles customer support queries",
                    "capabilities": ["problem_solving", "escalation"],
                    "tools": ["knowledge_base", "ticket_system"],
                    "model": settings.default_model,
                    "temperature": 0.5
                },
                {
                    "name": "researcher",
                    "role": "researcher",
                    "description": "Researches complex issues",
                    "capabilities": ["information_gathering", "analysis"],
                    "tools": ["web_search", "documentation_search"],
                    "model": settings.default_model,
                    "temperature": 0.7
                }
            ])
        
        elif config.chatbot_type == "technical_support":
            agents.extend([
                {
                    "name": "technical_analyst",
                    "role": "analyst",
                    "description": "Analyzes technical issues",
                    "capabilities": ["technical_analysis", "debugging"],
                    "tools": ["code_analysis", "log_analysis"],
                    "model": settings.default_model,
                    "temperature": 0.3
                },
                {
                    "name": "solution_provider",
                    "role": "specialist",
                    "description": "Provides technical solutions",
                    "capabilities": ["solution_generation", "code_generation"],
                    "tools": ["code_generator", "documentation"],
                    "model": settings.default_model,
                    "temperature": 0.6
                }
            ])
        
        # Add more agent types based on other chatbot types...
        
        return agents
    
    def _get_tools_for_config(self, config: ChatbotConfig) -> List[str]:
        """Get required tools based on configuration"""
        tools = ["conversation"]
        
        if config.enable_rag:
            tools.append("vector_search")
        
        if config.enable_function_calling:
            tools.append("function_calling")
        
        if config.enable_web_search:
            tools.append("web_search")
        
        for integration in config.integrations:
            if integration.get("type") == "rest_api":
                tools.append("api_client")
            elif integration.get("type") == "database":
                tools.append("database_query")
            elif integration.get("type") == "email":
                tools.append("email_client")
        
        return tools
