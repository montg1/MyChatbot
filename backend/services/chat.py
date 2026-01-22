"""
Chat service for handling n8n webhook integration.
"""
import httpx
import logging
from typing import List, Optional

from config import settings
from models import ChatMessage

logger = logging.getLogger(__name__)

# Resume content - can be moved to a database or file
RESUME_TEXT = """
NAME: Maverix

SUMMARY:
Software Engineer at NECTEC (National Electronics and Computer Technology Center),
specializing in AI/ML services and backend development. Core member of the 
Pathumma LLM Audio Team, responsible for building FastAPI services that power
Thailand's first multimodal audio-language AI model.

EXPERIENCE:
- Software Engineer, Pathumma Audio Team at NECTEC (Current)
  Building FastAPI backend services for Pathumma-llm-audio-1.0.0
  Developing inference APIs for 8B parameter Thai audio-language model
  Implementing model serving endpoints for speech, audio, and music processing
  Creating scalable API infrastructure using async Python and FastAPI

- Previous Experience
  Full-stack development with Python and JavaScript
  REST API design and implementation
  CI/CD pipeline setup and maintenance

PROJECTS:
- Pathumma LLM Audio 1.0.0: FastAPI service developer for Thailand's multimodal 
  audio-language model (8B parameters). Powers speech-to-text, audio understanding,
  and music analysis capabilities using OpenThaiLLM and Whisper-based architecture.
  Published on HuggingFace: nectec/Pathumma-llm-audio-1.0.0

- Resume Chatbot: AI-powered chatbot for interactive resume exploration
  using FastAPI backend and modern JavaScript frontend

SKILLS:
- Backend: FastAPI, Python, Async Programming, REST APIs, Uvicorn
- AI/ML: PyTorch, Transformers, HuggingFace, Model Serving, LLM APIs
- Languages: Python, JavaScript, TypeScript, SQL
- Cloud & DevOps: Docker, Kubernetes, LANTA Supercomputer, CI/CD
- Frontend: React, Vue.js, HTML/CSS, Vite
"""


class ChatService:
    """Service for handling chat requests via n8n webhook."""

    def __init__(self):
        self.webhook_url = settings.n8n_webhook_url
        self.resume_text = RESUME_TEXT
        self.timeout = 60.0

    async def get_response(
        self,
        message: str,
        session_id: str,
        history: Optional[List[ChatMessage]] = None,
    ) -> str:
        """
        Get AI response from n8n webhook.
        
        Args:
            message: User's question
            session_id: Session ID for context
            history: Previous chat messages
            
        Returns:
            AI-generated response string
        """
        if not self.webhook_url:
            logger.warning("N8N_WEBHOOK_URL not configured")
            return (
                "I'm sorry, the chat service is not configured. "
                "Please set the N8N_WEBHOOK_URL environment variable."
            )

        # Prepare payload
        payload = {
            "sessionId": session_id,
            "question": message,
            "resume_text": self.resume_text,
            "history": [msg.model_dump() for msg in (history or [])][-10:],
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.webhook_url, json=payload)
                response.raise_for_status()
                
                data = response.json()
                
                # Extract reply from various possible response formats
                reply = (
                    data.get("reply") or 
                    data.get("text") or 
                    data.get("output") or
                    str(data)
                )
                
                logger.info(f"Received response for session {session_id}")
                return reply

        except httpx.TimeoutException:
            logger.error(f"Timeout calling n8n webhook for session {session_id}")
            return "I'm sorry, the request timed out. Please try again."
        
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from n8n: {e.response.status_code}")
            return f"I'm sorry, there was an error processing your request. (HTTP {e.response.status_code})"
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return f"I'm sorry, an unexpected error occurred: {str(e)}"
