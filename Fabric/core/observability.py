"""
Observability integration for the Chatbot Factory
"""
import os
from typing import Optional, Dict, Any
from functools import wraps
import logging
from datetime import datetime

try:
    import opik
    from opik import track
    OPIK_AVAILABLE = True
except ImportError:
    OPIK_AVAILABLE = False

try:
    from langfuse import Langfuse
    from langfuse.decorators import observe
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False

from .config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ObservabilityManager:
    """Manages observability integrations"""
    
    def __init__(self):
        self.opik_client = None
        self.langfuse_client = None
        self._setup_clients()
    
    def _setup_clients(self):
        """Initialize observability clients"""
        
        # Setup Opik
        if OPIK_AVAILABLE and settings.opik_api_key:
            try:
                opik.configure(
                    api_key=settings.opik_api_key,
                    workspace=settings.opik_workspace
                )
                self.opik_client = opik
                logger.info("Opik client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Opik: {e}")
        
        # Setup Langfuse
        if LANGFUSE_AVAILABLE and settings.langfuse_secret_key:
            try:
                self.langfuse_client = Langfuse(
                    secret_key=settings.langfuse_secret_key,
                    public_key=settings.langfuse_public_key,
                    host=settings.langfuse_host
                )
                logger.info("Langfuse client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Langfuse: {e}")
    
    def track_generation(self, func):
        """Decorator to track chatbot generation"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            
            # Extract config if available
            config_data = {}
            if args and hasattr(args[0], 'dict'):
                config_data = args[0].dict()
            
            try:
                result = func(*args, **kwargs)
                
                # Log success
                self._log_event(
                    event_type="chatbot_generation",
                    status="success",
                    duration=(datetime.now() - start_time).total_seconds(),
                    metadata={
                        "config": config_data,
                        "result": result.dict() if hasattr(result, 'dict') else str(result)
                    }
                )
                
                return result
                
            except Exception as e:
                # Log error
                self._log_event(
                    event_type="chatbot_generation",
                    status="error",
                    duration=(datetime.now() - start_time).total_seconds(),
                    metadata={
                        "config": config_data,
                        "error": str(e)
                    }
                )
                raise
        
        return wrapper
    
    def track_llm_call(self, func):
        """Decorator to track LLM calls"""
        if self.opik_client and OPIK_AVAILABLE:
            return track(func)
        elif self.langfuse_client and LANGFUSE_AVAILABLE:
            return observe(func)
        else:
            return func
    
    def _log_event(self, event_type: str, status: str, duration: float, metadata: Dict[str, Any]):
        """Log events to observability platforms"""
        
        event_data = {
            "event_type": event_type,
            "status": status,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata
        }
        
        # Log to Opik
        if self.opik_client:
            try:
                # Opik logging would go here
                logger.info(f"Logged to Opik: {event_type}")
            except Exception as e:
                logger.warning(f"Failed to log to Opik: {e}")
        
        # Log to Langfuse
        if self.langfuse_client:
            try:
                self.langfuse_client.trace(
                    name=event_type,
                    metadata=event_data
                )
                logger.info(f"Logged to Langfuse: {event_type}")
            except Exception as e:
                logger.warning(f"Failed to log to Langfuse: {e}")
        
        # Always log locally
        logger.info(f"Event: {event_type} - Status: {status} - Duration: {duration}s")

# Global observability manager
observability = ObservabilityManager()
