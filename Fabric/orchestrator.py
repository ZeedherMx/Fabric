"""
Main Orchestrator - Coordinates the entire chatbot generation process using LangGraph
"""
import os
import asyncio
from typing import Dict, Any, List
from pathlib import Path
from langgraph import StateGraph, END
from langchain_groq import ChatGroq

from .core.models import ChatbotConfig, GenerationRequest, GenerationResponse
from .core.config import settings
from .core.observability import observability
from .agents.chatbot_architect import ChatbotArchitect
from .agents.code_generator import CodeGenerator

class ChatbotFactoryState(Dict[str, Any]):
    """State for the chatbot factory workflow"""
    pass

class ChatbotFactoryOrchestrator:
    """Main orchestrator for the chatbot factory"""
    
    def __init__(self):
        self.architect = ChatbotArchitect()
        self.code_generator = CodeGenerator()
        self.llm = ChatGroq(
            groq_api_key=settings.groq_api_key,
            model_name=settings.default_model,
            temperature=0.5
        )
        self.setup_workflow()
    
    def setup_workflow(self):
        """Setup the LangGraph workflow"""
        workflow = StateGraph(ChatbotFactoryState)
        
        # Add nodes
        workflow.add_node("validate_config", self.validate_config)
        workflow.add_node("design_architecture", self.design_architecture)
        workflow.add_node("generate_code", self.generate_code)
        workflow.add_node("create_docker", self.create_docker)
        workflow.add_node("finalize_output", self.finalize_output)
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "validate_config",
            self.should_continue_after_validation,
            {
                "continue": "design_architecture",
                "error": END
            }
        )
        
        workflow.add_edge("design_architecture", "generate_code")
        
        workflow.add_conditional_edges(
            "generate_code",
            self.should_create_docker,
            {
                "create_docker": "create_docker",
                "finalize": "finalize_output"
            }
        )
        
        workflow.add_edge("create_docker", "finalize_output")
        workflow.add_edge("finalize_output", END)
        
        # Set entry point
        workflow.set_entry_point("validate_config")
        
        self.workflow = workflow.compile()
    
    @observability.track_generation
    async def generate_chatbot(self, request: GenerationRequest) -> GenerationResponse:
        """Main method to generate a chatbot"""
        
        # Initialize state
        initial_state = {
            "config": request.config,
            "output_name": request.output_name,
            "include_tests": request.include_tests,
            "include_docs": request.include_docs,
            "errors": [],
            "generated_files": [],
            "success": False
        }
        
        try:
            # Run the workflow
            final_state = await self.workflow.ainvoke(initial_state)
            
            # Create response
            response = GenerationResponse(
                success=final_state.get("success", False),
                output_path=final_state.get("output_path", ""),
                message=final_state.get("message", ""),
                files_generated=final_state.get("generated_files", []),
                docker_image=final_state.get("docker_image"),
                errors=final_state.get("errors", [])
            )
            
            return response
            
        except Exception as e:
            return GenerationResponse(
                success=False,
                output_path="",
                message=f"Generation failed: {str(e)}",
                errors=[str(e)]
            )
    
    async def validate_config(self, state: ChatbotFactoryState) -> ChatbotFactoryState:
        """Validate the chatbot configuration"""
        config = state["config"]
        errors = []
        
        # Basic validation
        if not config.name or not config.name.strip():
            errors.append("Chatbot name is required")
        
        if not config.description or not config.description.strip():
            errors.append("Chatbot description is required")
        
        # Validate integrations
        for integration in config.integrations:
            if not integration.get("type"):
                errors.append("Integration type is required")
        
        # Validate multi-agent configuration
        if config.is_multi_agent and not config.agents:
            errors.append("Multi-agent system requires at least one agent configuration")
        
        # Check API key
        if not settings.groq_api_key:
            errors.append("GROQ_API_KEY is required")
        
        state["errors"] = errors
        state["validation_passed"] = len(errors) == 0
        
        if state["validation_passed"]:
            state["message"] = "Configuration validated successfully"
        else:
            state["message"] = f"Validation failed: {'; '.join(errors)}"
        
        return state
    
    async def design_architecture(self, state: ChatbotFactoryState) -> ChatbotFactoryState:
        """Design the chatbot architecture"""
        config = state["config"]
        
        try:
            architecture = await self.architect.design_architecture(config)
            state["architecture"] = architecture
            state["message"] = "Architecture designed successfully"
            
        except Exception as e:
            state["errors"].append(f"Architecture design failed: {str(e)}")
            state["message"] = f"Architecture design failed: {str(e)}"
        
        return state
    
    async def generate_code(self, state: ChatbotFactoryState) -> ChatbotFactoryState:
        """Generate the chatbot code"""
        config = state["config"]
        architecture = state["architecture"]
        output_name = state["output_name"]
        
        try:
            # Create output directory
            output_path = Path(settings.output_path) / output_name
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate code
            generated_files = await asyncio.to_thread(
                self.code_generator.generate_chatbot_code,
                config,
                architecture,
                str(output_path)
            )
            
            state["generated_files"] = generated_files
            state["output_path"] = str(output_path)
            state["message"] = f"Code generated successfully. {len(generated_files)} files created."
            
        except Exception as e:
            state["errors"].append(f"Code generation failed: {str(e)}")
            state["message"] = f"Code generation failed: {str(e)}"
        
        return state
    
    async def create_docker(self, state: ChatbotFactoryState) -> ChatbotFactoryState:
        """Create Docker image for the chatbot"""
        output_path = state["output_path"]
        config = state["config"]
        
        try:
            # Docker image name
            image_name = f"{config.name.lower().replace(' ', '-')}-chatbot"
            
            # Build Docker image (this would be implemented with actual Docker commands)
            # For now, we'll just simulate the process
            state["docker_image"] = f"{settings.docker_registry}/{image_name}:latest"
            state["message"] += " Docker configuration created."
            
        except Exception as e:
            state["errors"].append(f"Docker creation failed: {str(e)}")
            state["message"] += f" Docker creation failed: {str(e)}"
        
        return state
    
    async def finalize_output(self, state: ChatbotFactoryState) -> ChatbotFactoryState:
        """Finalize the output and cleanup"""
        
        # Generate additional files if requested
        if state.get("include_tests", False):
            await self._generate_tests(state)
        
        if state.get("include_docs", False):
            await self._generate_documentation(state)
        
        # Set success status
        state["success"] = len(state.get("errors", [])) == 0
        
        if state["success"]:
            state["message"] = f"Chatbot '{state['config'].name}' generated successfully!"
        else:
            state["message"] = f"Chatbot generation completed with errors: {'; '.join(state['errors'])}"
        
        return state
    
    def should_continue_after_validation(self, state: ChatbotFactoryState) -> str:
        """Decide whether to continue after validation"""
        return "continue" if state.get("validation_passed", False) else "error"
    
    def should_create_docker(self, state: ChatbotFactoryState) -> str:
        """Decide whether to create Docker configuration"""
        config = state["config"]
        return "create_docker" if config.enable_docker else "finalize"
    
    async def _generate_tests(self, state: ChatbotFactoryState):
        """Generate test files"""
        output_path = Path(state["output_path"])
        tests_dir = output_path / "tests"
        tests_dir.mkdir(exist_ok=True)
        
        # Generate basic test file
        test_content = f'''"""
Tests for {state["config"].name}
"""
import pytest
import asyncio
from main import {state["config"].name.replace(' ', '').replace('-', '')}Bot

@pytest.fixture
def chatbot():
    """Create chatbot instance for testing"""
    return {state["config"].name.replace(' ', '').replace('-', '')}Bot()

@pytest.mark.asyncio
async def test_basic_chat(chatbot):
    """Test basic chat functionality"""
    response = await chatbot.chat("Hello", [], "test_user")
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.asyncio
async def test_empty_message(chatbot):
    """Test handling of empty messages"""
    response = await chatbot.chat("", [], "test_user")
    assert isinstance(response, str)

# Add more tests based on configuration
'''
        
        test_file = tests_dir / "test_chatbot.py"
        with open(test_file, "w") as f:
            f.write(test_content)
        
        state["generated_files"].append(str(test_file))
    
    async def _generate_documentation(self, state: ChatbotFactoryState):
        """Generate additional documentation"""
        output_path = Path(state["output_path"])
        docs_dir = output_path / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        # Generate API documentation
        api_docs = f'''# {state["config"].name} API Documentation

## Overview
{state["config"].description}

## Endpoints

### POST /chat
Chat with the bot

**Request:**
```json
{{
  "message": "Hello!",
  "user_id": "user123"
}}
```

**Response:**
```json
{{
  "response": "Hello! How can I help you today?"
}}
```

## Configuration

The chatbot supports the following configuration options:

- **Type**: {state["config"].chatbot_type}
- **Personality**: {", ".join(state["config"].personality_traits)}
- **Domain Expertise**: {", ".join(state["config"].domain_expertise)}

## Deployment

See README.md for deployment instructions.
'''
        
        api_doc_file = docs_dir / "api.md"
        with open(api_doc_file, "w") as f:
            f.write(api_docs)
        
        state["generated_files"].append(str(api_doc_file))

# Global orchestrator instance
orchestrator = ChatbotFactoryOrchestrator()
