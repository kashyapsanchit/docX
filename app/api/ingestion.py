from fastapi import APIRouter, HTTPException, UploadFile, File, status, Form, Depends
from fastapi.responses import JSONResponse
from app.services.ingestion import Ingestion
from app.core.logger import logger  

router = APIRouter()

def get_ingestion_service() -> Ingestion:
    return Ingestion()

@router.post("/upload")
async def upload_document(
    title: str = Form(...), 
    document: UploadFile = File(...), 
    ingestion_service: Ingestion = Depends(get_ingestion_service)
):
    try:
        content = await document.read()
        ingestion_service.upload_document(title=title, content=content)
        await document.close() 

        return JSONResponse(
            content={"message": "Document uploaded successfully"},
            status_code=status.HTTP_201_CREATED
        )

    except Exception as e:
        logger.error(f"Upload failed for document '{title}': {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to upload document. Please try again later.")
