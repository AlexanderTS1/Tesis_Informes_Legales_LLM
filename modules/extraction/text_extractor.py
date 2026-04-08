import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io


def extraer_texto_pdf(pdf_path):
    """
    Extracción híbrida inteligente:
    - Intenta extraer texto estructural con PyMuPDF
    - Si una página no tiene texto, aplica OCR
    """

    texto_total = ""
    doc = fitz.open(pdf_path)

    for num_pagina, pagina in enumerate(doc, start=1):

        texto_pagina = pagina.get_text().strip()

        # Si la página tiene texto digital
        if texto_pagina:
            texto_total += f"\n\n--- Página {num_pagina} ---\n"
            texto_total += texto_pagina

        else:
            # Página escaneada → aplicar OCR
            pix = pagina.get_pixmap(dpi=300)  # Alta resolución
            img_bytes = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_bytes))

            texto_ocr = pytesseract.image_to_string(img, lang="spa")

            texto_total += f"\n\n--- Página {num_pagina} (OCR) ---\n"
            texto_total += texto_ocr

    doc.close()

    return texto_total.strip()
