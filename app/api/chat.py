from fastapi import APIRouter, HTTPException, UploadFile, Response, status, Form
from app.agent.graph import Graph
from app.agent.state import State
from app.core.logger import logger

router = APIRouter()

@router.post("/chat")
async def chat(session_id: str = Form(...), message: str = Form(...), doc_titles: list = Form(...)):

    try:
        agent = Graph()
        initial_state = {"query": message, "doc_titles": doc_titles}

        final_state = agent.graph.invoke(initial_state)
        
        return {"response": final_state['response']}    

    except Exception as e:
        logger.error(f"Error while uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
