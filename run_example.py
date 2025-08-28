"""
Example script to test the Chatbot Factory
"""
import asyncio
import os
from pathlib import Path

# Set up environment
os.environ["GROQ_API_KEY"] = "your_groq_api_key_here"  # Replace with actual key

from Fabric.core.models import ChatbotConfig, GenerationRequest, ChatbotType, PersonalityTrait
from Fabric.orchestrator import orchestrator

async def create_example_chatbot():
    """Create an example customer support chatbot"""
    
    # Define chatbot configuration
    config = ChatbotConfig(
        name="Customer Support Assistant",
        description="A helpful AI assistant for customer support queries",
        chatbot_type=ChatbotType.CUSTOMER_SUPPORT,
        personality_traits=[PersonalityTrait.PROFESSIONAL, PersonalityTrait.FRIENDLY, PersonalityTrait.EMPATHETIC],
        tone="professional",
        language="en",
        domain_expertise=["customer service", "product support", "troubleshooting"],
        knowledge_sources=["faq.txt", "product_manual.pdf"],
        enable_rag=True,
        enable_function_calling=True,
        enable_memory=True,
        enable_web_search=False,
        integrations=[
            {
                "type": "rest_api",
                "name": "Support Ticket API",
                "url": "https://api.example.com/tickets",
                "description": "Create and manage support tickets"
            }
        ],
        is_multi_agent=False,
        ui_theme="soft",
        port=7861,
        enable_docker=True
    )
    
    # Create generation request
    request = GenerationRequest(
        config=config,
        output_name="customer-support-bot",
        include_tests=True,
        include_docs=True
    )
    
    print("🤖 Generating Customer Support Chatbot...")
    print(f"📝 Name: {config.name}")
    print(f"🎯 Type: {config.chatbot_type}")
    print(f"🧠 Capabilities: RAG={config.enable_rag}, Memory={config.enable_memory}")
    print(f"📁 Output: {request.output_name}")
    print()
    
    try:
        # Generate the chatbot
        response = await orchestrator.generate_chatbot(request)
        
        if response.success:
            print("✅ Chatbot generated successfully!")
            print(f"📂 Output path: {response.output_path}")
            print(f"📄 Files generated: {len(response.files_generated)}")
            print(f"🐳 Docker image: {response.docker_image or 'Not created'}")
            print()
            print("Generated files:")
            for file_path in response.files_generated:
                print(f"  - {file_path}")
            print()
            print("🚀 To run your chatbot:")
            print(f"  cd {response.output_path}")
            print("  pip install -r requirements.txt")
            print("  python main.py")
            print()
            print("🐳 Or with Docker:")
            print(f"  cd {response.output_path}")
            print("  docker-compose up -d")
            
        else:
            print("❌ Chatbot generation failed!")
            print(f"Error: {response.message}")
            if response.errors:
                print("Errors:")
                for error in response.errors:
                    print(f"  - {error}")
    
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")

async def create_multi_agent_example():
    """Create an example multi-agent system"""
    
    config = ChatbotConfig(
        name="Technical Support Team",
        description="Multi-agent system for comprehensive technical support",
        chatbot_type=ChatbotType.TECHNICAL_SUPPORT,
        personality_traits=[PersonalityTrait.PROFESSIONAL, PersonalityTrait.DIRECT],
        tone="professional",
        domain_expertise=["software development", "system administration", "debugging"],
        enable_rag=True,
        enable_function_calling=True,
        enable_memory=True,
        is_multi_agent=True,
        agents=[
            {
                "name": "coordinator",
                "role": "coordinator",
                "description": "Routes technical queries to appropriate specialists",
                "capabilities": ["task_routing", "response_synthesis"]
            },
            {
                "name": "technical_analyst",
                "role": "analyst",
                "description": "Analyzes technical problems and errors",
                "capabilities": ["error_analysis", "log_analysis", "debugging"]
            },
            {
                "name": "solution_provider",
                "role": "specialist",
                "description": "Provides technical solutions and code examples",
                "capabilities": ["solution_generation", "code_generation"]
            }
        ],
        integrations=[
            {
                "type": "rest_api",
                "name": "GitHub API",
                "url": "https://api.github.com",
                "description": "Access code repositories and issues"
            }
        ],
        port=7862,
        enable_docker=True
    )
    
    request = GenerationRequest(
        config=config,
        output_name="technical-support-team",
        include_tests=True,
        include_docs=True
    )
    
    print("🤖 Generating Multi-Agent Technical Support System...")
    print(f"📝 Name: {config.name}")
    print(f"👥 Agents: {len(config.agents)}")
    print(f"🔧 Integrations: {len(config.integrations)}")
    print()
    
    try:
        response = await orchestrator.generate_chatbot(request)
        
        if response.success:
            print("✅ Multi-agent system generated successfully!")
            print(f"📂 Output path: {response.output_path}")
            print(f"📄 Files generated: {len(response.files_generated)}")
            print()
            print("🚀 Your multi-agent system is ready!")
            
        else:
            print("❌ Generation failed!")
            print(f"Error: {response.message}")
    
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")

async def main():
    """Run example generations"""
    print("🏭 Chatbot Factory - Example Generation")
    print("=" * 50)
    print()
    
    # Check if API key is set
    if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "your_groq_api_key_here":
        print("⚠️  Please set your GROQ_API_KEY in the script or environment")
        print("   You can get one from: https://console.groq.com/")
        return
    
    print("Example 1: Single Agent Customer Support Bot")
    print("-" * 45)
    await create_example_chatbot()
    
    print("\n" + "=" * 50 + "\n")
    
    print("Example 2: Multi-Agent Technical Support Team")
    print("-" * 47)
    await create_multi_agent_example()
    
    print("\n" + "=" * 50)
    print("🎉 Examples completed!")
    print()
    print("💡 Tips:")
    print("  - Customize the configurations above for your needs")
    print("  - Check the Output_Chatbot/ directory for generated bots")
    print("  - Use the web UI at http://localhost:7860/ui for easier configuration")

if __name__ == "__main__":
    asyncio.run(main())
