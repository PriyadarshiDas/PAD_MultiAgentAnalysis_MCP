from langchain.text_splitter import RecursiveCharacterTextSplitter
import fitz
import sys


def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    return " ".join([page.get_text() for page in doc])

def chunk_pdf(file_path):
    text = extract_text_from_pdf(file_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_text(text)
    return chunks
