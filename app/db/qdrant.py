from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from app.core.config import settings
from app.core.logger import logger

COLLECTION_NAME = "documents"

def get_qdrant_client() -> QdrantClient:
    """Initialize Qdrant client with settings."""
    try:
        client = QdrantClient(url=settings.QDRANT_HOST, api_key=settings.QDRANT_KEY, timeout=30)
        logger.info("Qdrant client initialized successfully.")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Qdrant client: {str(e)}")
        raise

def ensure_collection_exists(client: QdrantClient, collection_name: str, vector_size: int = 384):
    """Ensure the specified collection exists in Qdrant."""
    try:
        collections = client.get_collections().collections
        if collection_name not in [col.name for col in collections]:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            logger.info(f"Collection '{collection_name}' created successfully.")
        else:
            logger.info(f"Collection '{collection_name}' already exists.")
    except Exception as e:
        logger.error(f"Error ensuring collection '{collection_name}': {str(e)}")
        raise

qdrant_client = get_qdrant_client()
ensure_collection_exists(qdrant_client, COLLECTION_NAME)
