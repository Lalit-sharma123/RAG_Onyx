import fitz
import pytesseract
from PIL import Image
import io

def extract_text_with_ocr(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text()

        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image = Image.open(io.BytesIO(image_bytes))
            ocr_text = pytesseract.image_to_string(image)

            full_text += "\n" + ocr_text

    return full_text




###################check extract into graphs and charts 

# import fitz  # PyMuPDF
# import pytesseract
# from PIL import Image
# import io


# def extract_text_with_ocr(pdf_path):
#     doc = fitz.open(pdf_path)
#     full_text = ""

#     for page in doc:

#         # ---------------------------
#         # 1. EXTRACT NORMAL TEXT
#         # ---------------------------
#         page_text = page.get_text()
#         full_text += page_text + "\n"

#         # ---------------------------
#         # 2. EXTRACT IMAGES (GRAPHS / CHARTS)
#         # ---------------------------
#         for img in page.get_images(full=True):
#             xref = img[0]
#             base_image = doc.extract_image(xref)
#             image_bytes = base_image["image"]

#             image = Image.open(io.BytesIO(image_bytes))

#             # ---------------------------
#             # 🔥 IMPROVED OCR FOR GRAPHS
#             # ---------------------------
#             ocr_text = pytesseract.image_to_string(
#                 image,
#                 config="--oem 3 --psm 6"
#             )

#             full_text += "\n" + ocr_text + "\n"

#     return full_text