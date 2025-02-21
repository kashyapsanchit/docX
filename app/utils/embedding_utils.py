from sentence_transformers import SentenceTransformer
from app.core.logger import logger

# Pre-load the embedding model
# logger.info("Loading embedding model...")
# model = SentenceTransformer('all-MiniLM-L12-v2')


class EmbeddingUtils:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L12-v2')

    def generate_embedding(self, text: str) -> list:
        return self.model.encode(text).tolist()
    
