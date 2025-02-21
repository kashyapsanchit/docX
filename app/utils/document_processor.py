from io import BytesIO
from unstructured.partition.auto import partition
from app.core.logger import logger

def extract_data_from_document(content: bytes):
    with BytesIO(content) as buffer:
        elements = partition(file=buffer)

    text_data = []
    for element in elements:
        text_data.append(str(element))

    return text_data
