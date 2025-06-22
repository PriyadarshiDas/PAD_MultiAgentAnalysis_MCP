from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from chunking.chunk_pdf import chunk_pdf  # This now returns List[Document]

def setup_retriever(pdf_path):
    chunks = chunk_pdf(pdf_path)  # returns List[Document]

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)  # <-- updated line

    retriever = vectorstore.as_retriever()
    return retriever