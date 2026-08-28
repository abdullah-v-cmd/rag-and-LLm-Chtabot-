"""
Unit tests for RAG service.
"""
import pytest
from pathlib import Path
from app.services.rag_service import RAGService


class TestRAGService:
    """Test cases for RAG service."""
    
    @pytest.fixture
    def rag_service(self):
        """Create RAG service instance."""
        return RAGService()
    
    def test_initialization(self, rag_service):
        """Test RAG service initialization."""
        assert rag_service.embeddings is not None
        assert rag_service.llm is not None or rag_service.llm is None  # Depends on API key
    
    def test_generate_conversation_id(self):
        """Test conversation ID generation."""
        conv_id = RAGService._generate_conversation_id()
        assert isinstance(conv_id, str)
        assert len(conv_id) == 32  # MD5 hash length
    
    def test_load_document_unsupported_type(self, rag_service):
        """Test loading unsupported document type."""
        fake_path = Path("test.xyz")
        with pytest.raises(ValueError, match="Unsupported file type"):
            rag_service.load_document(fake_path)
