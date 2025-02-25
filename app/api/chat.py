from fastapi import APIRouter, HTTPException, UploadFile, Response, status, Form, Depends
from fastapi.responses import JSONResponse
from typing import List
from app.agent.graph import Graph
from app.core.logger import logger

router = APIRouter()

def get_graph() -> Graph:
    return Graph()

@router.post("/chat")
async def chat(
    session_id: str = Form(...),
    message: str = Form(...),
    doc_titles: List[str] = Form(...),
    agent: Graph = Depends(get_graph)
):
    try:

        if not message or not message.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty or whitespace")

        if not isinstance(doc_titles, list) or not doc_titles or not all(isinstance(title, str) and title.strip() for title in doc_titles):
            raise HTTPException(status_code=400, detail="Document titles must be a non-empty list of non-empty strings")
        
        initial_state = {"query": message, "doc_titles": doc_titles}
        final_state = agent.graph.invoke(initial_state)

        return JSONResponse(content={"response": final_state['response']}, status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error during chat invocation: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
