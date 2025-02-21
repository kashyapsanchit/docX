import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "http://localhost:6333")
    QDRANT_KEY: str = os.getenv("QDRANT_KEY", "")
    GROQ_KEY: str = os.getenv("GROQ_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "default")

settings = Settings()