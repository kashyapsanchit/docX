from sentence_transformers import SentenceTransformer
from typing import List
from app.core.logger import logger

class EmbeddingUtils:
    _model = None  

    def __init__(self):
        if EmbeddingUtils._model is None:
            try:
                logger.info("Loading embedding model: all-MiniLM-L12-v2...")
                EmbeddingUtils._model = SentenceTransformer('all-MiniLM-L12-v2')
                logger.info("Embedding model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {str(e)}")
                raise RuntimeError("Embedding model loading failed.")

        self.model = EmbeddingUtils._model

    def generate_embedding(self, text: str) -> List[float]:
        """Generates an embedding vector for the given text.

        Args:
            text (str): The input text.

        Returns:
            List[float]: The embedding vector.
        """
        if not text.strip():
            logger.warning("Empty text provided for embedding generation.")
            return []

        try:
            embedding = self.model.encode(text).tolist()
            logger.info(f"Generated embedding of length {len(embedding)}.")
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise RuntimeError("Embedding generation failed.")
