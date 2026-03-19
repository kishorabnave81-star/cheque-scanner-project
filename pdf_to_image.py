import os
import fitz  # PyMuPDF


def convert_pdf_to_images(pdf_path, output_folder, dpi=300):
    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)
    saved_paths = []

    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        output_path = os.path.join(output_folder, f"page_{i}.png")
        pix.save(output_path)
        saved_paths.append(output_path)

    doc.close()
    return saved_paths