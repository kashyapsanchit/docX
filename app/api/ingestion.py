from fastapi import APIRouter, HTTPException, UploadFile, File, Response, status, Form
from app.services.ingestion import Ingestion
from app.core.logger import logger  

router = APIRouter()

@router.post("/upload")
async def upload_document(title: str = Form(...), document: UploadFile = File(...)):

    try:
        ingestion_service = Ingestion()
        content = await document.read()

        ingestion_service.upload_document(title=title,content=content)
        return Response(content="Document uploaded successfully", status_code=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Error while uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
