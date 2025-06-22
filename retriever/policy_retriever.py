from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from chunking.chunk_pdf import chunk_pdf

def setup_retriever(pdf_path):
    chunks = chunk_pdf(pdf_path)

    #local embedding model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create vectorstore using FAISS
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)

    retriever = vectorstore.as_retriever()
    return retriever
