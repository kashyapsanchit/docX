import uvicorn
from fastapi import FastAPI
from app.api import ingestion, chat


app = FastAPI(title="docX - Document Q/A System")

app.include_router(ingestion.router, prefix="/ingestion", tags=["Ingestion"])
app.include_router(chat.router, tags=["Chat"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
