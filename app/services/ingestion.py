import uuid
import hashlib
from typing import List
from app.db.qdrant import qdrant_client
from app.utils.embedding_utils import EmbeddingUtils
from app.utils.document_processor import extract_data_from_document
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
from app.core.config import settings
from app.core.logger import logger

class Ingestion(EmbeddingUtils):
    def __init__(self, qdrant_client=qdrant_client, collection_name: str = None):
        super().__init__()
        self.qdrant_client = qdrant_client
        self.collection_name = collection_name or settings.QDRANT_COLLECTION_NAME

    def _compute_document_hash(self, content: bytes) -> str:
        """Generate SHA-256 hash of the document content."""
        return hashlib.sha256(content).hexdigest()

    def _check_duplicate(self, doc_hash: str) -> bool:
        """Check if a document with the given hash already exists."""
        search_filter = Filter(
            must=[
                FieldCondition(key="doc_hash", match=MatchValue(value=doc_hash))
            ]
        )
        search_result = self.qdrant_client.scroll(
            collection_name=self.collection_name,
            scroll_filter=search_filter,
            limit=1  
        )
        return bool(search_result[0])  
    
    def upload_document(self, title: str, content: bytes):
        """Extract, embed, and upload document to Qdrant with duplicate prevention."""
        try:
            doc_hash = self._compute_document_hash(content)
            logger.info(f"Computed hash for '{title}': {doc_hash}")

            if self._check_duplicate(doc_hash):
                logger.warning(f"Duplicate detected for '{title}'. Skipping upload.")
                raise ValueError("Duplicate document detected")

            document_id = str(uuid.uuid4())
            text_data = extract_data_from_document(content)
            points = self._prepare_points(text_data, title, document_id, doc_hash)

            self._upsert_points(points)
            logger.info(f"Document '{title}' uploaded successfully with ID {document_id}")

        except ValueError as ve:
            raise ve  
        except Exception as e:
            logger.error(f"Error uploading document '{title}': {str(e)}")
            raise RuntimeError(f"Failed to upload document: {str(e)}")

    def _prepare_points(self, text_data: List[str], title: str, document_id: str, doc_hash: str) -> List[PointStruct]:
        """Generate embeddings and prepare Qdrant points with doc_hash."""
        return [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=self.generate_embedding(text),
                payload={
                    "id": document_id,
                    "text": text,
                    "title": title,
                    "doc_hash": doc_hash  
                }
            )
            for text in text_data
        ]

    def _upsert_points(self, points: List[PointStruct], batch_size: int = 100):
        """Upsert points into Qdrant with batching."""
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=batch
            )
