"""
FastAPI Backend for Resume Chatbot
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from config import settings
from models import ChatRequest, ChatResponse, HealthResponse
from services.chat import ChatService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize chat service
chat_service = ChatService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("🚀 Resume Chatbot API starting up...")
    yield
    logger.info("👋 Resume Chatbot API shutting down...")


app = FastAPI(
    title="Resume Chatbot API",
    description="Backend API for the Resume + Chatbot application",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return AI response.
    
    - **message**: The user's question about the resume
    - **sessionId**: Unique session identifier for conversation context
    - **history**: Optional list of previous messages for context
    """
    try:
        reply = await chat_service.get_response(
            message=request.message,
            session_id=request.sessionId,
            history=request.history,
        )
        return ChatResponse(reply=reply)
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get response: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
