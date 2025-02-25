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
- **Run the backend**: Inside the project folder run the following command.
```bash
uvicorn app.main:app --reload
```
- **Run the frontend**: Inside the project folder run the following command.
```bash
streamlit run streamlit_app.py
```
- **Access**: The project will be up and running at `http://localhost:8501`

