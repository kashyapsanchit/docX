import uuid
from typing import List
from app.db.qdrant import qdrant_client, COLLECTION_NAME
from app.utils.embedding_utils import EmbeddingUtils
from app.utils.document_processor import extract_data_from_document
from qdrant_client.models import PointStruct
from app.core.logger import logger

class Ingestion(EmbeddingUtils):
    def __init__(self, qdrant_client=qdrant_client):
        super().__init__()
        self.qdrant_client = qdrant_client

    def upload_document(self, title: str, content: bytes):
        """Extract, embed, and upload document to Qdrant."""
        try:
            document_id = str(uuid.uuid4())
            text_data = extract_data_from_document(content)
            points = self._prepare_points(text_data, title, document_id)

            self._upsert_points(points)
            logger.info(f"Document '{title}' uploaded successfully with ID {document_id}")

        except Exception as e:
            logger.error(f"Error uploading document '{title}': {str(e)}")
            raise RuntimeError(f"Failed to upload document: {str(e)}")

    def _prepare_points(self, text_data: List[str], title: str, document_id: str) -> List[PointStruct]:
        """Generate embeddings and prepare Qdrant points."""
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=self.generate_embedding(text),
                payload={"id": document_id, "text": text, "title": title}
            )
            for text in text_data
        ]
        return points

    def _upsert_points(self, points: List[PointStruct], batch_size: int = 100):
        """Upsert points into Qdrant with batching."""
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.qdrant_client.upsert(collection_name=COLLECTION_NAME, points=batch)
