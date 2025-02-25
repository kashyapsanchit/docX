import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

@pytest.mark.order(1)
def test_missing_title():
    """Test document upload without a title."""
    with open("tests/Attention.pdf", "rb") as file:
        response = client.post(
            "/ingestion/upload", 
            files={"document": file}  
        )
    assert response.status_code == 422

@pytest.mark.order(2)
def test_missing_file():
    """Test document upload without a file."""
    response = client.post(
        "/ingestion/upload", 
        data={"title": "Attention is all you need"}  
    )
    assert response.status_code == 422

@pytest.mark.order(3)
def test_invalid_file_type():
    """Test uploading an unsupported file type."""
    with open("tests/invalid_file.txt", "rb") as file:
        response = client.post(
            "/ingestion/upload", 
            files={"document": file},
            data={"title": "Attention is all you need"}
        )
    assert response.status_code == 400  
    assert response.json()["detail"] == "Unsupported file format."

@pytest.mark.order(4)
def test_empty_file_upload():
    """Test uploading an empty file."""
    with open("tests/empty_file.pdf", "rb") as file:
        response = client.post(
            "/ingestion/upload", 
            files={"document": file},
            data={"title": "Attention is all you need"}
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is empty"

@pytest.mark.order(5)
def test_duplicate_document_upload():
    """Test uploading the same document twice to check for deduplication."""
    with open("tests/Attention.pdf", "rb") as file:
        response = client.post(
            "/ingestion/upload", 
            files={"document": file},
            data={"title": "Attention is all you need"}
        )
    
    assert response.status_code == 500 

