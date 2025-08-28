"""
Simple demo version of the Chatbot Factory
"""
import gradio as gr
import json
from typing import Dict, Any

def create_demo_interface():
    """Create a simplified demo interface"""
    
    def generate_chatbot_demo(name, description, chatbot_type, personality_traits, 
                             enable_rag, enable_memory, enable_function_calling,
                             domain_expertise, output_name):
        """Demo chatbot generation function"""
        
        if not name or not output_name:
            return "❌ Error: Name and output name are required", ""
        
        # Simulate generation process
        config = {
            "name": name,
            "description": description,
            "type": chatbot_type,
            "personality": personality_traits,
            "capabilities": {
                "rag": enable_rag,
                "memory": enable_memory,
                "function_calling": enable_function_calling
            },
            "domain_expertise": domain_expertise.split(",") if domain_expertise else [],
            "output_name": output_name
        }
        
        # Simulate successful generation
        result = {
            "success": True,
            "message": f"✅ Chatbot '{name}' generated successfully!",
            "output_path": f"./Output_Chatbot/{output_name}",
            "files_generated": [
                f"./Output_Chatbot/{output_name}/main.py",
                f"./Output_Chatbot/{output_name}/requirements.txt",
                f"./Output_Chatbot/{output_name}/Dockerfile",
                f"./Output_Chatbot/{output_name}/README.md",
                f"./Output_Chatbot/{output_name}/config.json"
            ],
            "docker_image": f"{output_name}:latest"
        }
        
        status_msg = f"""🎉 Generation Complete!

📝 Chatbot Name: {name}
🎯 Type: {chatbot_type}
🧠 Capabilities: RAG={enable_rag}, Memory={enable_memory}, Functions={enable_function_calling}
📁 Output: {output_name}

🚀 Next Steps:
1. Navigate to: ./Output_Chatbot/{output_name}/
2. Install dependencies: pip install -r requirements.txt
3. Run: python main.py
4. Or use Docker: docker-compose up -d

📄 Generated Files:
• main.py - Complete chatbot application
• requirements.txt - Python dependencies  
• Dockerfile - Container configuration
• docker-compose.yml - Multi-service setup
• README.md - Usage instructions
• config.json - Runtime configuration
"""
        
        return status_msg, json.dumps(result, indent=2)
    
    # Create the interface
    with gr.Blocks(title="🤖 Chatbot Factory Demo", theme=gr.themes.Soft()) as demo:
        
        gr.Markdown("# 🤖 Chatbot Factory")
        gr.Markdown("Generate fully functional AI chatbots with custom configurations")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("## Basic Configuration")
                
                name = gr.Textbox(
                    label="Chatbot Name",
                    placeholder="Customer Support Assistant",
                    value="Customer Support Bot"
                )
                
                description = gr.Textbox(
                    label="Description", 
                    placeholder="A helpful AI assistant for customer support",
                    lines=2,
                    value="A professional AI assistant that helps customers with their queries and provides excellent support."
                )
                
                chatbot_type = gr.Dropdown(
                    label="Chatbot Type",
                    choices=["customer_support", "sales_assistant", "knowledge_base", "creative_assistant", "technical_support"],
                    value="customer_support"
                )
                
                personality_traits = gr.CheckboxGroup(
                    label="Personality Traits",
                    choices=["professional", "friendly", "casual", "formal", "humorous", "empathetic"],
                    value=["professional", "friendly", "empathetic"]
                )
            
            with gr.Column():
                gr.Markdown("## Capabilities")
                
                enable_rag = gr.Checkbox(
                    label="Enable RAG (Knowledge Base)",
                    value=True,
                    info="Allow chatbot to search knowledge base"
                )
                
                enable_memory = gr.Checkbox(
                    label="Enable Conversation Memory", 
                    value=True,
                    info="Remember conversation history"
                )
                
                enable_function_calling = gr.Checkbox(
                    label="Enable Function Calling",
                    value=True,
                    info="Allow external API calls"
                )
                
                domain_expertise = gr.Textbox(
                    label="Domain Expertise",
                    placeholder="customer service, product support, troubleshooting",
                    value="customer service, product support, billing"
                )
                
                output_name = gr.Textbox(
                    label="Output Folder Name",
                    placeholder="my-chatbot",
                    value="customer-support-bot"
                )
        
        with gr.Row():
            generate_btn = gr.Button("🚀 Generate Chatbot", variant="primary", size="lg")
        
        with gr.Row():
            with gr.Column():
                status_output = gr.Textbox(
                    label="Generation Status",
                    lines=15,
                    interactive=False
                )
            
            with gr.Column():
                json_output = gr.Code(
                    label="Generation Results (JSON)",
                    language="json",
                    lines=15,
                    interactive=False
                )
        
        # Connect the generate button
        generate_btn.click(
            fn=generate_chatbot_demo,
            inputs=[name, description, chatbot_type, personality_traits, 
                   enable_rag, enable_memory, enable_function_calling,
                   domain_expertise, output_name],
            outputs=[status_output, json_output]
        )
        
        gr.Markdown("""
        ## 🎯 About This Demo
        
        This is a **demonstration** of the Chatbot Factory system. In the full version:
        
        - **LangGraph Orchestration**: Sophisticated AI workflow management
        - **Groq Integration**: High-performance LLM inference  
        - **Real Code Generation**: Actual Python applications with FastAPI + Gradio
        - **Multi-Agent Systems**: Teams of specialized AI agents
        - **Docker Ready**: Complete containerization
        - **Observability**: Opik/Langfuse integration
        - **Advanced Features**: RAG, function calling, memory, integrations
        
        ### 🏗️ System Architecture
        ```
        Fabric/                 # Core factory system
        ├── agents/            # AI agents (architect, code generator)  
        ├── core/              # Configuration and models
        ├── templates/         # Chatbot templates
        └── ui/               # This interface
        
        Output_Chatbot/        # Generated chatbots live here
        ```
        
        ### 🚀 Generated Chatbots Include:
        - Complete Python application (FastAPI + Gradio)
        - Docker configuration for deployment
        - Requirements and documentation
        - Test files and API endpoints
        - Custom UI themes and styling
        """)
    
    return demo

if __name__ == "__main__":
    demo = create_demo_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
