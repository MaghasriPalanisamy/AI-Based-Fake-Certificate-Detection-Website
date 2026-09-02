import os
import fitz


# ======================================================
# PDF to Image Converter (PyMuPDF)
# ======================================================
def pdf_to_image(pdf_path):
    """
    Convert the first page of a PDF into a PNG image
    using PyMuPDF (fitz).
    """

    try:

        print("\n========== PDF CONVERSION ==========")
        print("Input PDF :", pdf_path)

        doc = fitz.open(pdf_path)

        page = doc.load_page(0)

        # High resolution for OCR
        matrix = fitz.Matrix(3, 3)

        pix = page.get_pixmap(matrix=matrix)

        image_path = os.path.splitext(pdf_path)[0] + ".png"

        pix.save(image_path)

        doc.close()

        print("Output Image :", image_path)
        print("Image Exists :", os.path.exists(image_path))
        print("====================================\n")

        return image_path

    except Exception as e:

        print("\n========== PDF CONVERSION ERROR ==========")
        print(e)
        print("==========================================")

        return pdf_path