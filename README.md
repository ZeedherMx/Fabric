# 🤖 Chatbot Factory

An AI-powered system that generates fully functional chatbots based on user specifications. Built with LangGraph, Groq, and modern observability tools.

## 🌟 Features

- **LangGraph Orchestration**: Sophisticated workflow management for chatbot generation
- **Groq Integration**: High-performance LLM inference
- **Observability**: Built-in support for Opik and Langfuse
- **Multi-Agent Systems**: Generate teams of specialized AI agents
- **RAG Capabilities**: Knowledge retrieval and augmentation
- **Function Calling**: External API and tool integration
- **Docker Ready**: Complete containerization support
- **Gradio UI**: User-friendly web interface
- **FastAPI Backend**: RESTful API for programmatic access

## 🏗️ Architecture

```
chatbot-factory/
├── Fabric/                 # Core factory system
│   ├── core/              # Configuration and models
│   ├── agents/            # AI agents (architect, code generator)
│   ├── templates/         # Chatbot templates
│   ├── ui/               # Gradio interface
│   └── utils/            # Utilities
├── Output_Chatbot/        # Generated chatbots
├── main.py               # Application entry point
├── requirements.txt      # Dependencies
├── Dockerfile           # Container configuration
└── docker-compose.yml  # Multi-service setup
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker (optional)
- Groq API key

### Installation

1. **Clone and setup:**
   ```bash
   git clone <repository>
   cd chatbot-factory
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the factory:**
   ```bash
   python main.py
   ```

4. **Access the UI:**
   - Web Interface: http://localhost:7860/ui
   - API Documentation: http://localhost:7860/docs

### Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 🎯 Usage

### Web Interface

1. **Configure**: Set chatbot parameters in the Configuration tab
2. **Preview**: Review your configuration and predicted architecture
3. **Generate**: Create your chatbot with one click
4. **Deploy**: Use the generated Docker files for deployment

### API Usage

```python
import requests

# Generate a chatbot
response = requests.post("http://localhost:7860/generate", json={
    "config": {
        "name": "Customer Support Bot",
        "description": "Helpful customer service assistant",
        "chatbot_type": "customer_support",
        "personality_traits": ["professional", "friendly"],
        "enable_rag": True,
        "enable_memory": True
    },
    "output_name": "customer-bot",
    "include_tests": True,
    "include_docs": True
})

print(response.json())
```

## 🔧 Configuration Options

### Chatbot Types
- **Customer Support**: Help desk and support queries
- **Sales Assistant**: Lead qualification and sales support
- **Knowledge Base**: Information retrieval and Q&A
- **Creative Assistant**: Content creation and brainstorming
- **Technical Support**: Code help and troubleshooting
- **Multi-Agent Team**: Specialized agent collaboration

### Capabilities
- **RAG**: Vector search and knowledge retrieval
- **Function Calling**: External API integration
- **Memory**: Conversation history persistence
- **Web Search**: Real-time information access

### Integrations
- REST APIs
- Databases
- Email systems
- Slack/Discord
- Webhooks
- File systems

## 🧠 Multi-Agent Systems

The factory can generate sophisticated multi-agent systems with specialized roles:

- **Coordinator**: Routes tasks between agents
- **Researcher**: Gathers information
- **Analyst**: Processes and analyzes data
- **Writer**: Creates content and responses
- **Reviewer**: Quality control and validation
- **Specialist**: Domain-specific expertise

## 📊 Observability

Built-in integration with leading observability platforms:

### Opik Integration
```bash
export OPIK_API_KEY=your_key
export OPIK_WORKSPACE=your_workspace
```

### Langfuse Integration
```bash
export LANGFUSE_SECRET_KEY=your_secret
export LANGFUSE_PUBLIC_KEY=your_public_key
export LANGFUSE_HOST=https://cloud.langfuse.com
```

## 🔌 Generated Chatbot Structure

Each generated chatbot includes:

```
my-chatbot/
├── main.py              # Main application
├── agents/              # Agent implementations
├── ui/                  # UI configuration
├── config.json          # Chatbot configuration
├── requirements.txt     # Dependencies
├── Dockerfile          # Container setup
├── docker-compose.yml  # Multi-service config
├── README.md           # Usage instructions
├── tests/              # Test files (optional)
└── docs/               # Documentation (optional)
```

## 🛠️ Development

### Adding New Agent Types

1. Create agent class in `Fabric/agents/`
2. Update `ChatbotArchitect` to include new agent logic
3. Add templates in `Fabric/templates/`
4. Update UI options in `gradio_interface.py`

### Custom Templates

Add new templates in `Fabric/templates/` following the existing pattern:

```python
CUSTOM_TEMPLATE = '''
# Your custom chatbot template
# Use Jinja2 templating syntax
'''
```

### Testing

```bash
# Run tests
pytest tests/

# Generate test chatbot
python -c "
from Fabric.core.models import *
from Fabric.orchestrator import orchestrator
import asyncio

config = ChatbotConfig(name='Test Bot', description='Test chatbot')
request = GenerationRequest(config=config, output_name='test-bot')
result = asyncio.run(orchestrator.generate_chatbot(request))
print(result)
"
```

## 📈 Performance

- **Generation Time**: 30-60 seconds per chatbot
- **Concurrent Generations**: Up to 5 simultaneous
- **Output Size**: 50-200 KB per generated chatbot
- **Memory Usage**: ~500MB base + 100MB per generation

## 🔒 Security

- API key encryption in transit
- No sensitive data logging
- Isolated Docker containers
- Rate limiting on API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Issues**: GitHub Issues
- **Documentation**: `/docs` endpoint
- **API Reference**: `/docs` endpoint when running

## 🎉 Examples

Check the `examples/` directory for sample configurations and generated chatbots.

---

**Built with ❤️ using LangGraph, Groq, and modern AI tools**
