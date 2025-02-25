import pytest
from app.db.qdrant import get_qdrant_client, ensure_collection_exists
from app.core.config import settings
from fastapi.testclient import TestClient
from app.main import app
import logging

logger = logging.getLogger(__name__)

test_client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_ingestion():
    """Run ingestion before all tests"""
    with open("tests/Attention.pdf", "rb") as file:
        response = test_client.post(
            "/ingestion/upload",
            files={"document": file},
            data={"title": "Attention is all you need"}
        )

    if response.status_code != 201:
        logger.error(f"Ingestion failed: {response.status_code} - {response.json()}")
        pytest.fail("Failed to ingest document before tests")
    else:
        logger.info("Ingestion successful for 'Attention is all you need'")

    yield  

    qdrant_client = get_qdrant_client()

    qdrant_client.delete_collection(collection_name=settings.QDRANT_COLLECTION_NAME)
