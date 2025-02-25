from fastapi import APIRouter, HTTPException, UploadFile, File, status, Form, Depends
from fastapi.responses import JSONResponse
from app.services.ingestion import Ingestion
from app.core.logger import logger
import os

router = APIRouter()

ALLOWED_FILE_TYPES = ["application/pdf"]
MAX_FILE_SIZE_MB = 10  

def get_ingestion_service() -> Ingestion:
    return Ingestion()

@router.post("/upload")
async def upload_document(
    title: str = Form(...),
    document: UploadFile = File(...),
    ingestion_service: Ingestion = Depends(get_ingestion_service)
):
    try:
        if not title.strip():
            raise HTTPException(status_code=400, detail="Document title cannot be empty")

        if document.content_type not in ALLOWED_FILE_TYPES:
            raise HTTPException(status_code=400, detail="Unsupported file format.")

        content = await document.read()

        file_size_mb = len(content) / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            raise HTTPException(status_code=400, detail=f"File size exceeds {MAX_FILE_SIZE_MB} MB limit")

        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        ingestion_service.upload_document(title=title, content=content)
        await document.close()

        return JSONResponse(
            content={"message": "Document uploaded successfully"},
            status_code=status.HTTP_201_CREATED
        )

    except HTTPException as he:
        logger.warning(f"Client error for document '{title}': {he.detail}")
        raise he  

    except Exception as e:
        logger.error(f"Upload failed for document '{title}': {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to upload document. Please try again later.")
