import uuid
from app.db.qdrant import qdrant_client, COLLECTION_NAME
from app.utils.embedding_utils import EmbeddingUtils
from app.utils.document_processor import extract_data_from_document
from qdrant_client.models import PointStruct
from app.core.logger import logger


class Ingestion(EmbeddingUtils):

    def __init__(self):
        super().__init__()

    def upload_document(self, title, content):

        try:

            points = []
            text_data = extract_data_from_document(content)
            id = str(uuid.uuid4())

            for text in text_data:
                
                embedding = self.generate_embedding(str(text))
                points.append(
                    PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embedding,
                        payload={"id": id, "text": text, "title": title}  
                    )
                )

            qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)
        
        except Exception as e:
            logger.error(f"Error while uploading document: {str(e)}")
            raise ValueError(f"Error while uploading document: {str(e)}")
