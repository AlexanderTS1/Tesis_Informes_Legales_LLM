import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import os

def es_pdf_escaneado(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                return False
    return True

def extraer_texto_pdf(pdf_path):
    texto = ""

    if not es_pdf_escaneado(pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                texto += page.extract_text() + "\n"
    else:
        images = convert_from_path(pdf_path)
        for img in images:
            texto += pytesseract.image_to_string(img, lang="spa") + "\n"

    return texto.strip()
