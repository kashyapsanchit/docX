# Document Retrieval Q/A RAG System

The Document Retrieval Q/A RAG System leverages FastAPI, Qdrant, and the all-MiniLM-L12-v2 model to generate, store, and retrieve embeddings. Utilizing the LangGraph ReAct agent, the system processes user queries and generates accurate responses based on the retrieved data.

## Key Components

- **FastAPI**: Serves as the backend framework to handle API requests and manage interactions between components.
- **Qdrant**: Acts as the vector database for storing and retrieving embeddings efficiently.
- **all-MiniLM-L12-v2**: Used for generating high-quality text embeddings to power the retrieval process.
- **LangGraph ReAct Agent**: Facilitates intelligent query processing and response generation with tool usage.
- **Streamlit**: Provides an interactive frontend where users can upload documents, select specific documents to query, and view results.

## Features

- **Document Upload**: Users can upload documents directly through the Streamlit interface.
- **Selective Querying**: Users can choose specific documents to include in the Q&A process.
- **Efficient Retrieval**: Utilizes Qdrant’s vector search capabilities for fast and accurate data retrieval.
- **Interactive Frontend**: Streamlit interface ensures a user-friendly experience for uploading, selecting, and querying documents.

This system integrates powerful tools to deliver an efficient and flexible document-based Q&A experience, catering to diverse user needs.

## Setting up the project

- **Clone the repository**: Clone the repository using the below command.
```bash
git clone https://github.com/kashyapsanchit/docX.git
```
- **Create a virtual environment**: In the cloned folder create a virtual environment and activate it.
```bash
python3 -m venv env
source env/bin/activate
.\env\Scripts\activate # For Windows
```
- **Install Dependencies**: Install all the dependencies in the requirements.txt file.
```bash
pip install -r requirements.txt
```
- **Create .env**: Create and add the below required environment variables.
```bash
QDRANT_HOST="{your_qdrant_host}"
QDRANT_KEY="{your_qdrant_key}"
MODEL_NAME="llama-3.1-8b-instant" # In this example we have used llama-3.1-8b as our LLM. 
GROQ_KEY="{your_groq_key}" 
ENV="development"
QDRANT_COLLECTION_NAME="documents"
```

- **Spin up the server**: Inside the project folder run the following commands.
```bash
uvicorn app.main:app --reload
streamlit run streamlit_app.py
```
- **Access**: The project will be up and running at `http://localhost:8501`

## Running using Docker
- **Run using Docker**: Alternatively you can also run using docker using the following command:
```bash
docker-compose up --build
```

## Running Tests

- Tests have been written using the fastapi testclient alongwith pytest.
- **Change .env for testing**: Change the below parameters in the .env before running tests.
```bash
ENV="testing"
QDRANT_COLLECTION_NAME="test_documents"
```
- Doing so ensures that the main collection is not affected due to testcases.
- Cleanup is done after tests complete so that no test data persists in the cloud vector store.

- **Run**: Run tests using the below after you have done all the required changes:
```bash
pytest
```