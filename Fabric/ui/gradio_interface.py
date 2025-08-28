"""
Gradio UI for the Chatbot Factory
"""
import gradio as gr
import asyncio
import json
from typing import Dict, Any, List, Tuple
from pathlib import Path

from ..core.models import ChatbotConfig, GenerationRequest, ChatbotType, PersonalityTrait, IntegrationType
from ..orchestrator import orchestrator
from ..core.config import settings

class ChatbotFactoryUI:
    """Gradio interface for the chatbot factory"""
    
    def __init__(self):
        self.current_config = None
        self.generation_history = []
    
    def create_interface(self) -> gr.Blocks:
        """Create the main Gradio interface"""
        
        with gr.Blocks(
            title="🤖 Chatbot Factory",
            theme=gr.themes.Soft(),
            css=self._get_custom_css()
        ) as interface:
            
            gr.Markdown("# 🤖 Chatbot Factory")
            gr.Markdown("Generate fully functional AI chatbots with custom configurations")
            
            with gr.Tabs():
                # Configuration Tab
                with gr.Tab("⚙️ Configuration"):
                    config_components = self._create_config_tab()
                
                # Preview Tab
                with gr.Tab("👀 Preview"):
                    preview_components = self._create_preview_tab()
                
                # Generation Tab
                with gr.Tab("🚀 Generate"):
                    generation_components = self._create_generation_tab()
                
                # History Tab
                with gr.Tab("📜 History"):
                    history_components = self._create_history_tab()
            
            # Connect components
            self._connect_components(config_components, preview_components, generation_components, history_components)
        
        return interface
    
    def _create_config_tab(self) -> Dict[str, Any]:
        """Create the configuration tab"""
        components = {}
        
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("## Basic Information")
                
                components["name"] = gr.Textbox(
                    label="Chatbot Name",
                    placeholder="My Awesome Chatbot",
                    info="Give your chatbot a unique name"
                )
                
                components["description"] = gr.Textbox(
                    label="Description",
                    placeholder="A helpful AI assistant for customer support",
                    lines=3,
                    info="Describe what your chatbot does"
                )
                
                components["chatbot_type"] = gr.Dropdown(
                    label="Chatbot Type",
                    choices=[e.value for e in ChatbotType],
                    value=ChatbotType.CUSTOMER_SUPPORT.value,
                    info="Select the primary purpose of your chatbot"
                )
                
                gr.Markdown("## Personality & Behavior")
                
                components["personality_traits"] = gr.CheckboxGroup(
                    label="Personality Traits",
                    choices=[e.value for e in PersonalityTrait],
                    value=[PersonalityTrait.PROFESSIONAL.value, PersonalityTrait.FRIENDLY.value],
                    info="Select personality traits for your chatbot"
                )
                
                components["tone"] = gr.Dropdown(
                    label="Communication Tone",
                    choices=["professional", "casual", "formal", "friendly", "humorous"],
                    value="professional"
                )
                
                components["language"] = gr.Dropdown(
                    label="Primary Language",
                    choices=["en", "es", "fr", "de", "it", "pt", "zh", "ja"],
                    value="en"
                )
            
            with gr.Column(scale=2):
                gr.Markdown("## Capabilities")
                
                components["enable_rag"] = gr.Checkbox(
                    label="Enable RAG (Retrieval-Augmented Generation)",
                    value=True,
                    info="Allow chatbot to search and use knowledge base"
                )
                
                components["enable_function_calling"] = gr.Checkbox(
                    label="Enable Function Calling",
                    value=True,
                    info="Allow chatbot to call external functions/APIs"
                )
                
                components["enable_memory"] = gr.Checkbox(
                    label="Enable Conversation Memory",
                    value=True,
                    info="Remember conversation history"
                )
                
                components["enable_web_search"] = gr.Checkbox(
                    label="Enable Web Search",
                    value=False,
                    info="Allow chatbot to search the web for information"
                )
                
                gr.Markdown("## Domain Expertise")
                
                components["domain_expertise"] = gr.Textbox(
                    label="Areas of Expertise",
                    placeholder="customer service, technical support, sales",
                    info="Comma-separated list of expertise areas"
                )
                
                components["knowledge_sources"] = gr.Textbox(
                    label="Knowledge Sources",
                    placeholder="company_docs.pdf, faq.txt, knowledge_base.json",
                    info="Comma-separated list of knowledge source files"
                )
                
                gr.Markdown("## Multi-Agent System")
                
                components["is_multi_agent"] = gr.Checkbox(
                    label="Enable Multi-Agent System",
                    value=False,
                    info="Create a team of specialized AI agents"
                )
                
                components["agent_roles"] = gr.CheckboxGroup(
                    label="Agent Roles (for multi-agent systems)",
                    choices=["coordinator", "researcher", "analyst", "writer", "reviewer", "specialist"],
                    visible=False,
                    info="Select roles for your agent team"
                )
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("## Integrations")
                
                components["integrations_json"] = gr.Code(
                    label="Integrations Configuration (JSON)",
                    language="json",
                    value='[\n  {\n    "type": "rest_api",\n    "name": "External API",\n    "url": "https://api.example.com",\n    "auth": "bearer_token"\n  }\n]',
                    lines=10,
                    info="Configure external integrations"
                )
            
            with gr.Column():
                gr.Markdown("## UI Configuration")
                
                components["ui_theme"] = gr.Dropdown(
                    label="UI Theme",
                    choices=["default", "soft", "monochrome", "glass"],
                    value="default"
                )
                
                components["port"] = gr.Number(
                    label="Port",
                    value=7860,
                    minimum=1000,
                    maximum=65535
                )
                
                components["logo_url"] = gr.Textbox(
                    label="Logo URL (optional)",
                    placeholder="https://example.com/logo.png"
                )
                
                components["custom_css"] = gr.Code(
                    label="Custom CSS (optional)",
                    language="css",
                    lines=5
                )
                
                components["enable_docker"] = gr.Checkbox(
                    label="Generate Docker Configuration",
                    value=True,
                    info="Create Docker files for easy deployment"
                )
        
        # Update agent roles visibility based on multi-agent checkbox
        components["is_multi_agent"].change(
            fn=lambda x: gr.update(visible=x),
            inputs=[components["is_multi_agent"]],
            outputs=[components["agent_roles"]]
        )
        
        return components
    
    def _create_preview_tab(self) -> Dict[str, Any]:
        """Create the preview tab"""
        components = {}
        
        gr.Markdown("## Configuration Preview")
        gr.Markdown("Review your chatbot configuration before generation")
        
        components["preview_json"] = gr.Code(
            label="Configuration JSON",
            language="json",
            lines=20,
            interactive=False
        )
        
        components["preview_button"] = gr.Button(
            "🔄 Update Preview",
            variant="secondary"
        )
        
        components["architecture_preview"] = gr.Code(
            label="Predicted Architecture",
            language="json",
            lines=15,
            interactive=False
        )
        
        return components
    
    def _create_generation_tab(self) -> Dict[str, Any]:
        """Create the generation tab"""
        components = {}
        
        gr.Markdown("## Generate Your Chatbot")
        
        with gr.Row():
            with gr.Column():
                components["output_name"] = gr.Textbox(
                    label="Output Folder Name",
                    placeholder="my-awesome-chatbot",
                    info="Name for the generated chatbot folder"
                )
                
                components["include_tests"] = gr.Checkbox(
                    label="Include Test Files",
                    value=True
                )
                
                components["include_docs"] = gr.Checkbox(
                    label="Include Documentation",
                    value=True
                )
            
            with gr.Column():
                components["generate_button"] = gr.Button(
                    "🚀 Generate Chatbot",
                    variant="primary",
                    size="lg"
                )
                
                components["generation_status"] = gr.Textbox(
                    label="Status",
                    interactive=False,
                    lines=3
                )
        
        components["generation_output"] = gr.Code(
            label="Generation Results",
            language="json",
            lines=15,
            interactive=False
        )
        
        components["download_button"] = gr.File(
            label="Download Generated Chatbot",
            visible=False
        )
        
        return components
    
    def _create_history_tab(self) -> Dict[str, Any]:
        """Create the history tab"""
        components = {}
        
        gr.Markdown("## Generation History")
        
        components["history_table"] = gr.Dataframe(
            headers=["Name", "Type", "Generated", "Status", "Files"],
            datatype=["str", "str", "str", "str", "number"],
            interactive=False
        )
        
        components["refresh_history"] = gr.Button("🔄 Refresh History")
        
        return components
    
    def _connect_components(self, config_components, preview_components, generation_components, history_components):
        """Connect all components with their functions"""
        
        # Preview functionality
        preview_components["preview_button"].click(
            fn=self._update_preview,
            inputs=list(config_components.values()),
            outputs=[preview_components["preview_json"], preview_components["architecture_preview"]]
        )
        
        # Generation functionality
        generation_components["generate_button"].click(
            fn=self._generate_chatbot,
            inputs=list(config_components.values()) + [
                generation_components["output_name"],
                generation_components["include_tests"],
                generation_components["include_docs"]
            ],
            outputs=[
                generation_components["generation_status"],
                generation_components["generation_output"],
                generation_components["download_button"]
            ]
        )
        
        # History functionality
        history_components["refresh_history"].click(
            fn=self._refresh_history,
            outputs=[history_components["history_table"]]
        )
    
    def _update_preview(self, *args) -> Tuple[str, str]:
        """Update the configuration preview"""
        try:
            config = self._create_config_from_inputs(*args)
            config_json = json.dumps(config.dict(), indent=2)
            
            # Simulate architecture preview
            architecture_preview = {
                "type": "multi_agent" if config.is_multi_agent else "single_agent",
                "agents": len(config.agents) if config.agents else 1,
                "capabilities": {
                    "rag": config.enable_rag,
                    "function_calling": config.enable_function_calling,
                    "memory": config.enable_memory,
                    "web_search": config.enable_web_search
                },
                "integrations": len(config.integrations),
                "estimated_files": 8 + (3 if config.enable_docker else 0)
            }
            
            architecture_json = json.dumps(architecture_preview, indent=2)
            
            return config_json, architecture_json
            
        except Exception as e:
            return f"Error: {str(e)}", f"Error: {str(e)}"
    
    def _generate_chatbot(self, *args) -> Tuple[str, str, gr.File]:
        """Generate the chatbot"""
        try:
            # Extract generation parameters
            *config_args, output_name, include_tests, include_docs = args
            
            if not output_name or not output_name.strip():
                return "Error: Output name is required", "", gr.File(visible=False)
            
            config = self._create_config_from_inputs(*config_args)
            
            request = GenerationRequest(
                config=config,
                output_name=output_name,
                include_tests=include_tests,
                include_docs=include_docs
            )
            
            # Run generation in async context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                response = loop.run_until_complete(orchestrator.generate_chatbot(request))
            finally:
                loop.close()
            
            # Update history
            self.generation_history.append({
                "name": config.name,
                "type": config.chatbot_type,
                "generated": "Just now",
                "status": "Success" if response.success else "Failed",
                "files": len(response.files_generated)
            })
            
            status = f"✅ Success: {response.message}" if response.success else f"❌ Error: {response.message}"
            output_json = json.dumps(response.dict(), indent=2)
            
            # Create download file if successful
            download_file = None
            if response.success and response.output_path:
                # In a real implementation, you'd create a zip file here
                download_file = gr.File(value=None, visible=True)
            
            return status, output_json, download_file or gr.File(visible=False)
            
        except Exception as e:
            return f"❌ Error: {str(e)}", f'{{"error": "{str(e)}"}}', gr.File(visible=False)
    
    def _refresh_history(self) -> List[List[str]]:
        """Refresh the generation history"""
        return [[h["name"], h["type"], h["generated"], h["status"], str(h["files"])] for h in self.generation_history]
    
    def _create_config_from_inputs(self, *args) -> ChatbotConfig:
        """Create ChatbotConfig from UI inputs"""
        (name, description, chatbot_type, personality_traits, tone, language,
         enable_rag, enable_function_calling, enable_memory, enable_web_search,
         domain_expertise, knowledge_sources, is_multi_agent, agent_roles,
         integrations_json, ui_theme, port, logo_url, custom_css, enable_docker) = args
        
        # Parse domain expertise
        domain_list = [d.strip() for d in domain_expertise.split(",") if d.strip()] if domain_expertise else []
        
        # Parse knowledge sources
        knowledge_list = [k.strip() for k in knowledge_sources.split(",") if k.strip()] if knowledge_sources else []
        
        # Parse integrations
        try:
            integrations = json.loads(integrations_json) if integrations_json else []
        except json.JSONDecodeError:
            integrations = []
        
        # Create agent configurations for multi-agent systems
        agents = []
        if is_multi_agent and agent_roles:
            for role in agent_roles:
                agents.append({
                    "name": f"{role}_agent",
                    "role": role,
                    "description": f"Specialized {role} agent",
                    "capabilities": [role]
                })
        
        return ChatbotConfig(
            name=name,
            description=description,
            chatbot_type=chatbot_type,
            personality_traits=personality_traits,
            tone=tone,
            language=language,
            domain_expertise=domain_list,
            knowledge_sources=knowledge_list,
            enable_rag=enable_rag,
            enable_function_calling=enable_function_calling,
            enable_memory=enable_memory,
            enable_web_search=enable_web_search,
            integrations=integrations,
            is_multi_agent=is_multi_agent,
            agents=agents,
            ui_theme=ui_theme,
            port=int(port),
            logo_url=logo_url if logo_url else None,
            custom_css=custom_css if custom_css else None,
            enable_docker=enable_docker
        )
    
    def _get_custom_css(self) -> str:
        """Get custom CSS for the interface"""
        return """
        .gradio-container {
            max-width: 1200px !important;
        }
        
        .tab-nav {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        
        .generate-button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            color: white;
            font-weight: bold;
        }
        
        .status-success {
            color: #10b981;
            font-weight: bold;
        }
        
        .status-error {
            color: #ef4444;
            font-weight: bold;
        }
        """

# Create global UI instance
ui = ChatbotFactoryUI()
