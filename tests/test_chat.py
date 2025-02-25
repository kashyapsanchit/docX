import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.order(6)
def test_chat_query():
    """Test valid chat query with proper form data."""
    data = {
        "session_id": str(uuid.uuid4()),
        "message": "What is Multi-Head Attention mechanism?",
        "doc_titles": ["Attention is all you need"]
    }
    response = client.post("/chat", data=data)
    assert response.status_code == 200
    assert "response" in response.json()
    assert isinstance(response.json()["response"], str)
    assert response.json()["response"] != "", "Response should not be empty"

@pytest.mark.order(7)
def test_invalid_query_empty_message():
    """Test chat query with an empty message field."""
    data = {
        "session_id": str(uuid.uuid4()),
        "message": "",
        "doc_titles": ["Attention is all you need"]
    }
    response = client.post("/chat", data=data)
    assert response.status_code == 500

@pytest.mark.order(8)
def test_empty_doc_titles():
    """Test chat query with empty document titles."""
    data = {
        "session_id": str(uuid.uuid4()),
        "message": "What is attention mechanism?",
        "doc_titles": []
    }
    response = client.post("/chat", data=data)
    assert response.status_code == 422
