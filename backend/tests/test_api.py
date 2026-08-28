"""
API endpoint tests.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test health check returns 200."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "services" in data


class TestChatEndpoint:
    """Test chat endpoint."""
    
    def test_chat_without_documents(self):
        """Test chat returns error without documents."""
        response = client.post(
            "/api/chat",
            json={
                "message": "Hello",
                "use_rag": True
            }
        )
        # May return 400 or 500 depending on vector store state
        assert response.status_code in [400, 500]


class TestDocumentEndpoint:
    """Test document endpoints."""
    
    def test_list_documents(self):
        """Test listing documents."""
        response = client.get("/api/documents")
        assert response.status_code == 200
        data = response.json()
        assert "documents" in data
        assert "total" in data
        assert isinstance(data["documents"], list)
