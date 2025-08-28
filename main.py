"""
Main entry point for the Chatbot Factory
"""
import os
import sys
import asyncio
import uvicorn
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from Fabric.core.config import settings
from Fabric.core.models import GenerationRequest, GenerationResponse
from Fabric.orchestrator import orchestrator
from Fabric.ui.gradio_interface import ui

# Create FastAPI app
app = FastAPI(
    title="Chatbot Factory API",
    description="Generate fully functional AI chatbots with custom configurations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to the Chatbot Factory!",
        "version": "1.0.0",
        "docs": "/docs",
        "ui": "/ui"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "chatbot-factory"}

@app.post("/generate", response_model=GenerationResponse)
async def generate_chatbot(request: GenerationRequest):
    """Generate a chatbot via API"""
    try:
        response = await orchestrator.generate_chatbot(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/templates")
async def list_templates():
    """List available chatbot templates"""
    templates_path = Path(settings.templates_path)
    if not templates_path.exists():
        return {"templates": []}
    
    templates = []
    for template_file in templates_path.glob("*.json"):
        templates.append(template_file.stem)
    
    return {"templates": templates}

@app.get("/history")
async def get_generation_history():
    """Get generation history"""
    # This would typically come from a database
    return {"history": ui.generation_history}

# Create Gradio interface
gradio_app = ui.create_interface()

# Mount Gradio app
app = gr.mount_gradio_app(app, gradio_app, path="/ui")

def main():
    """Main function to run the application"""
    print("🤖 Starting Chatbot Factory...")
    print(f"📊 Observability: {'Enabled' if settings.opik_api_key or settings.langfuse_secret_key else 'Disabled'}")
    print(f"🔧 Groq API: {'Configured' if settings.groq_api_key else 'Not configured'}")
    print(f"📁 Output Path: {settings.output_path}")
    print(f"🌐 UI will be available at: http://localhost:7860/ui")
    print(f"📚 API docs will be available at: http://localhost:7860/docs")
    
    # Ensure output directory exists
    Path(settings.output_path).mkdir(parents=True, exist_ok=True)
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=7860,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
