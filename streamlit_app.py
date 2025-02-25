import streamlit as st
import requests
import uuid
from PIL import Image
from app.db.qdrant import qdrant_client
from app.core.config import settings

def get_uploaded_documents():
    """Fetch uploaded documents."""

    response = qdrant_client.scroll(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        scroll_filter=None,
        limit=1000 
    )

    titles = set(point.payload.get("title") for point in response[0] if point.payload.get("title"))
    return list(titles)


st.set_page_config(
    page_title="docX",  
    layout="wide"
)

st.title("📑 docX - Document Q/A")

if "selected_docs" not in st.session_state:
    st.session_state.selected_docs = []

with st.sidebar:
    st.header("Settings")
    
    st.subheader("Select Documents")
    doc_titles = get_uploaded_documents()

    for title in doc_titles:
        if st.sidebar.checkbox(title, key=title, value=title in st.session_state.selected_docs):
            if title not in st.session_state.selected_docs:
                st.session_state.selected_docs.append(title)
        else:
            if title in st.session_state.selected_docs:
                st.session_state.selected_docs.remove(title)

    st.subheader("Upload Documents")
    document = st.file_uploader(label="Upload", type=["txt", "md", "pdf"], label_visibility="hidden")
    title = st.text_input("Title")
    
    if st.button("Upload") and document and title:
        files = {"document": document}
        data = {"title": title}

        response = requests.post("http://localhost:8000/ingestion/upload", files=files, data=data)
        
        st.session_state.document = None
        st.session_state.title = ""

        st.success(f"✅ '{title}' uploaded successfully!")
        st.rerun()
    

if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  

# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

if prompt := st.chat_input("How can I help you today?"):

    if len(st.session_state.selected_docs) != 0:

        st.session_state.messages.append(prompt)

        with st.chat_message("user"):
            st.markdown(prompt)

        data = {"session_id": st.session_state.session_id, "message": prompt, "doc_titles": st.session_state.selected_docs}

        response = requests.post(
            "http://localhost:8000/chat",
            data=data
        )
        
        response = response.json()
        bot_message = response.get('response', None)

        st.session_state.messages.append({"role": "assistant", "content": bot_message})
        
        with st.chat_message("assistant"):
            st.markdown(bot_message)
    
    else:
        st.dialog("Please select at least one document to proceed.")
