"""
Chat API endpoints for conversational interactions.
"""
from fastapi import APIRouter, HTTPException
import logging

from app.models.schemas import ChatRequest, ChatResponse
from app.services.rag_service import rag_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for conversational AI with RAG support.
    
    - **message**: User's message/question
    - **conversation_id**: Optional conversation ID for context
    - **use_rag**: Whether to use RAG for context (default: True)
    - **max_tokens**: Maximum tokens in response
    - **temperature**: LLM temperature (0.0 - 2.0)
    """
    try:
        logger.info(f"Received chat request: {request.message[:50]}...")
        
        if request.use_rag:
            # Use RAG for context-aware response
            result = rag_service.query(
                question=request.message,
                conversation_id=request.conversation_id,
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
            
            return ChatResponse(
                message=result['answer'],
                conversation_id=result['conversation_id'],
                sources=result.get('sources'),
                metadata={
                    'used_rag': True,
                    'model': 'gpt-3.5-turbo'
                }
            )
        else:
            # Direct LLM response without RAG
            raise HTTPException(
                status_code=501,
                detail="Direct LLM chat without RAG not yet implemented"
            )
            
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history (placeholder for future implementation)."""
    raise HTTPException(
        status_code=501,
        detail="Conversation history not yet implemented"
    )
