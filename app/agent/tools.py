from langchain.tools import StructuredTool
from app.utils.embedding_utils import EmbeddingUtils
from app.core.logger import logger
from qdrant_client.models import Filter, FieldCondition, MatchValue
from app.db.qdrant import qdrant_client, COLLECTION_NAME

def search_document(query: str, doc_titles: list = None):
    """Fetches relevant data from documents in Qdrant collection based on query and document titles"""
    try:
        if not query:
            raise ValueError("Query cannot be empty.")
        if not doc_titles:
            raise ValueError("Document titles cannot be empty.")
        import pdb; pdb.set_trace()

        embedding_utils = EmbeddingUtils()
        query_embedding = embedding_utils.generate_embedding(query)

        search_filter = Filter(
            should=[FieldCondition(key="title", match=MatchValue(value=doc)) for doc in doc_titles]
        )

        response = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            query_filter=search_filter,
            limit=30
        )

        if not response:
            return {
                "response": f"No relevant information found in '{doc_titles}' for the query."
            }
        

        return {
            "response": " ".join([point.payload['text'] for point in response])
        }

    except Exception as e:
        logger.error(f"Error while searching document: {str(e)}")
        raise ValueError(f"Error while searching document: {str(e)}")


search_document_tool = StructuredTool.from_function(
    name="search_document",
    description="""Search relevant data from documents in Qdrant collection based on query and document titles.
    Parameters:
    - query: str
    - doc_titles: list[str]
    Returns:
    - response: dict
    """,
    func=search_document
)

tools = [search_document_tool]
