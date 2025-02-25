from langchain.tools import StructuredTool
from app.utils.embedding_utils import EmbeddingUtils
from app.core.logger import logger
from qdrant_client.models import Filter, FieldCondition, MatchValue
from app.db.qdrant import qdrant_client
from typing import List, Dict, Optional
from app.core.config import settings

def search_document(query: str, doc_titles: List[str], limit: int = 30, client=qdrant_client) -> Dict[str, str]:
    """Fetches relevant data from documents in Qdrant collection based on query and document titles.

    Args:
        query (str): User's search query.
        doc_titles (List[str]): List of document titles to search within.
        limit (int): Max number of results to return. Defaults to 30.
        client (QdrantClient): Instance of the Qdrant client.

    Returns:
        Dict[str, str]: Search results or error message.
    """
    try:
        if not query.strip():
            raise ValueError("Query cannot be empty.")
        if not doc_titles:
            raise ValueError("Document titles cannot be empty.")

        logger.info(f"Generating embedding for query: {query}")
        embedding_utils = EmbeddingUtils()
        query_embedding = embedding_utils.generate_embedding(query)

        search_filter = Filter(
            should=[FieldCondition(key="title", match=MatchValue(value=doc)) for doc in doc_titles]
        )

        logger.info(f"Performing search in collection '{settings.QDRANT_COLLECTION_NAME}' with limit {limit}")
        response = client.query_points(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query=query_embedding,
            query_filter=search_filter,
            limit=limit
        )

        if not response:
            logger.info(f"No results found for query: {query}")
            return {
                "response": f"No relevant information found in '{doc_titles}' for the query."
            }

        combined_text = " ".join([point.payload['text'] for point in response])
        logger.info(f"Found {len(response)} matching documents.")
        return {"response": combined_text}

    except ValueError as ve:
        logger.warning(f"Validation error: {str(ve)}")
        raise ve
    except Exception as e:
        logger.error(f"Error while searching document: {str(e)}")
        raise RuntimeError(f"Search failed: {str(e)}")


search_document_tool = StructuredTool.from_function(
    name="search_document",
    description="""Search relevant data from documents in Qdrant collection based on query and document titles.
    Parameters:
    - query: str
    - doc_titles: list[str]
    - limit: int (optional, defaults to 30)
    Returns:
    - response: dict
    """,
    func=search_document
)

tools = [search_document_tool]
