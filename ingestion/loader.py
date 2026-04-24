import fitz  # PyMuPDF correct 
from pathlib import Path


def load_txt_files(path="data/documents"):
    docs = []
    for file in Path(path).glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            docs.append(f.read())
    return docs


def load_pdf(file_path) :
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


def load_pdfs(path="data/documents"):
    docs = []
    for file in Path(path).glob("*.pdf"):
        docs.append(load_pdf(file))
    return docs


def load_documents(path="data/documents"):
    docs = []

    docs.extend(load_txt_files(path))
    docs.extend(load_pdfs(path))   # 🔥 THIS IS THE KEY LINE

    return docs






