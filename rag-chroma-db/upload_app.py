from typing import List

import streamlit as st
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from chroma_client import DEFAULT_COLLECTION, get_vectorstore


# ---------------- Page Config ----------------
st.set_page_config(page_title="Chroma Cloud Ingest", layout="wide")
st.title("Chroma Cloud Ingest")
st.caption("Upload files or paste text to build a RAG index.")


# ---------------- Sidebar ----------------
with st.sidebar:
    st.subheader("Collection")
    collection_name = st.text_input("Collection name", value=DEFAULT_COLLECTION)

    st.subheader("Chunking")
    chunk_size = st.number_input("Chunk size", min_value=200, max_value=400, value=300)

    chunk_overlap = st.number_input(
        "Chunk overlap", min_value=0, max_value=100, value=20
    )


# ---------------- Text Input ----------------
st.subheader("Paste Text")
text_source = st.text_input("Source label", value="manual")
raw_text = st.text_area("Paste content", height=220)


# ---------------- File Upload ----------------
st.subheader("Upload Files")
uploaded_files = st.file_uploader(
    "Supported types: .txt, .md, .pdf",
    type=["txt", "md", "pdf"],
    accept_multiple_files=True,
)


# ---------------- Helper Functions ----------------
def documents_from_text(text: str, source: str) -> List[Document]:
    if not text.strip():
        return []

    return [Document(page_content=text, metadata={"source": source})]


def documents_from_upload(files) -> List[Document]:
    documents = []

    for uploaded in files:
        filename = uploaded.name.lower()

        # PDF
        if filename.endswith(".pdf"):
            reader = PdfReader(uploaded)

            text = "\n".join(
                page.extract_text() for page in reader.pages if page.extract_text()
            )

        # TXT / MD
        else:
            text = uploaded.read().decode("utf-8")

        if text.strip():
            documents.append(
                Document(page_content=text, metadata={"source": uploaded.name})
            )

    return documents


# ---------------- Ingest ----------------
if st.button("Ingest into Chroma"):

    documents = []

    # manual text
    documents.extend(documents_from_text(raw_text, text_source))

    # uploaded files
    documents.extend(documents_from_upload(uploaded_files or []))

    if not documents:
        st.warning("Add some text or upload files.")
        st.stop()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_documents(documents)

    # Get vectorstore
    vectorstore = get_vectorstore()

    # Add to Chroma
    vectorstore.add_documents(chunks)

    st.success(f"Ingested {len(chunks)} chunks successfully.")
