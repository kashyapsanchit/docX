from io import BytesIO
from unstructured.partition.auto import partition
from typing import List
from app.core.logger import logger

def extract_data_from_document(content: bytes) -> List[str]:
    """Extracts text data from a document using unstructured's partition method.
    Args:
        content (bytes): The byte content of the document.
    Returns:
        List[str]: A list of extracted text elements.
    """
    
    try:
        if not content:
            logger.warning("Empty document provided for extraction.")
            return []

        with BytesIO(content) as buffer:
            elements = partition(file=buffer)

        text_data = [str(element) for element in elements]

        logger.info(f"Extracted {len(text_data)} text elements from the document.")
        return text_data

    except Exception as e:
        logger.error(f"Error during document extraction: {str(e)}")
        raise RuntimeError("Failed to extract data from document.")
