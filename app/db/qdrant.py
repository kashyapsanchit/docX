from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from app.core.config import settings

qdrant_client = QdrantClient(url=settings.QDRANT_HOST, api_key=settings.QDRANT_KEY, timeout=30)

COLLECTION_NAME = "documents"

collections = qdrant_client.get_collections().collections

if COLLECTION_NAME not in [col.name for col in collections]:
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
                    size=384,  
                    distance=Distance.COSINE  
                )
    )


