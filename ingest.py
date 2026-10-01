"""
ingest.py — Load the college FAQ document, split into chunks,
            generate embeddings, and save the FAISS vector store.

Run this ONCE before starting the app:
    python ingest.py
"""

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DATA_PATH = "data/college_faq.txt"
FAISS_INDEX_PATH = "faiss_index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def build_vector_store():
    print("[1/4] Loading FAQ document...")
    loader = TextLoader(DATA_PATH, encoding="utf-8")
    documents = loader.load()

    print("[2/4] Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        separators=["\n\n", "\n", ".", " "],
    )
    chunks = splitter.split_documents(documents)
    print(f"      -> {len(chunks)} chunks created")

    print("[3/4] Generating embeddings (this may take a minute)...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
    )

    print("[4/4] Building and saving FAISS index...")
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(FAISS_INDEX_PATH)
    print(f"DONE! FAISS index saved to '{FAISS_INDEX_PATH}/'")


if __name__ == "__main__":
    build_vector_store()
