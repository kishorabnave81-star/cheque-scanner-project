import fitz   # PyMuPDF
import os

INPUT_FOLDER = "../input_pdfs"
OUTPUT_FOLDER = "../output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for file in os.listdir(INPUT_FOLDER):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(INPUT_FOLDER, file)
        print("Processing:", pdf_path)

        doc = fitz.open(pdf_path)

        for page_number in range(len(doc)):
            page = doc.load_page(page_number)

            pix = page.get_pixmap(dpi=300)

            output_path = os.path.join(OUTPUT_FOLDER, f"page_{page_number+1}.png")

            pix.save(output_path)

            print("Saved:", output_path)

print("Done")