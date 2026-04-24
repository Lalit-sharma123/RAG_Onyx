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





##########################check
# import fitz  # PyMuPDF
# from pathlib import Path
# import pdfplumber


# # ---------------------------
# # TXT FILES (WITH METADATA)
# # ---------------------------
# def load_txt_files(path="data/documents"):
#     docs = []

#     for file in Path(path).glob("*.txt"):
#         with open(file, "r", encoding="utf-8") as f:
#             docs.append({
#                 "text": f.read(),
#                 "page": None,
#                 "type": "text",
#                 "source": str(file)
#             })

#     print(f"📄 Loaded {len(docs)} TXT files")
#     return docs


# # ---------------------------
# # PDF TEXT (PAGE-WISE)
# # ---------------------------
# def load_pdf_text(file_path):
#     doc = fitz.open(file_path)
#     docs = []

#     for page_num, page in enumerate(doc):
#         text = page.get_text().strip()

#         if text:
#             docs.append({
#                 "text": text,
#                 "page": page_num + 1,
#                 "type": "text",
#                 "source": str(file_path)
#             })

#     print(f"📄 Extracted {len(docs)} pages (text)")
#     return docs


# # ---------------------------
# # TABLE EXTRACTION (IMPORTANT)
# # ---------------------------
# def load_pdf_tables(file_path):
#     docs = []

#     with pdfplumber.open(file_path) as pdf:
#         for page_num, page in enumerate(pdf.pages):

#             tables = page.extract_tables()

#             for table in tables:
#                 table_text = "\n".join(
#                     [" | ".join([str(cell) for cell in row]) for row in table]
#                 )

#                 docs.append({
#                     "text": table_text,
#                     "page": page_num + 1,
#                     "type": "table",
#                     "source": str(file_path)
#                 })

#     print(f"📊 Extracted {len(docs)} tables")
#     return docs


# # ---------------------------
# # MAIN PDF LOADER (STRUCTURED)
# # ---------------------------
# def load_pdf(file_path):

#     print(f"\n📄 Processing PDF: {file_path}")

#     docs = []

#     # 🔹 text
#     docs.extend(load_pdf_text(file_path))

#     # 🔹 tables
#     docs.extend(load_pdf_tables(file_path))

#     print(f"✅ Total structured elements: {len(docs)}")

#     return docs


# # ---------------------------
# # LOAD ALL DOCUMENTS
# # ---------------------------
# def load_pdfs(path="data/documents"):
#     docs = []

#     for file in Path(path).glob("*.pdf"):
#         docs.extend(load_pdf(file))  # 🔥 important change

#     return docs


# def load_documents(path="data/documents"):
#     docs = []

#     docs.extend(load_txt_files(path))
#     docs.extend(load_pdfs(path))

#     print(f"\n📦 TOTAL DOCUMENTS LOADED: {len(docs)}")

#     return docs