"""
Simple test to verify the system structure
"""
import os
import sys
from pathlib import Path

def test_structure():
    """Test the project structure"""
    print("🧪 Testing Chatbot Factory Structure")
    print("=" * 40)
    
    # Check main directories
    required_dirs = [
        "Fabric",
        "Fabric/core", 
        "Fabric/agents",
        "Fabric/ui",
        "Fabric/templates",
        "Output_Chatbot"
    ]
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path}")
    
    print()
    
    # Check main files
    required_files = [
        "main.py",
        "requirements.txt",
        "Dockerfile",
        "docker-compose.yml",
        "README.md",
        "Fabric/core/models.py",
        "Fabric/core/config.py",
        "Fabric/agents/chatbot_architect.py",
        "Fabric/agents/code_generator.py",
        "Fabric/orchestrator.py",
        "Fabric/ui/gradio_interface.py"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
    
    print()
    print("🎯 System Structure Test Complete!")
    print()
    print("📋 Next Steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set up environment: cp .env.example .env")
    print("3. Add your GROQ_API_KEY to .env")
    print("4. Run the system: python main.py")
    print("5. Access UI at: http://localhost:7860/ui")

if __name__ == "__main__":
    test_structure()
