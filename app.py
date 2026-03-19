import os
import sys
import tempfile
import pandas as pd
import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

from pdf_to_image import convert_pdf_to_images
from gemini_extract import extract_cheque_data
from validate_cheque import validate_cheque_data
from export_cheque_data import build_final_row

st.set_page_config(page_title="Cheque Scanner", layout="wide")

st.title("Cheque Scanner & Data Extractor")
st.write("Upload a cheque PDF, extract structured data, validate it, and download Excel output.")

uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])

if uploaded_file is not None:
    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, uploaded_file.name)

        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success("PDF uploaded successfully.")

        if st.button("Process PDF"):
            progress = st.progress(0)
            status = st.empty()

            raw_output_folder = os.path.join(temp_dir, "raw_images")
            os.makedirs(raw_output_folder, exist_ok=True)

            status.text("Step 1/3: Converting PDF to images...")
            convert_pdf_to_images(pdf_path, raw_output_folder)
            progress.progress(33)

            image_files = sorted(
                [
                    os.path.join(raw_output_folder, f)
                    for f in os.listdir(raw_output_folder)
                    if f.lower().endswith(".png")
                ]
            )

            status.text("Step 2/3: Extracting and validating cheque data...")
            all_rows = []

            for img_path in image_files:
                extracted_data = extract_cheque_data(img_path)

                if "error" in extracted_data:
                    row = {
                        "source_file": os.path.basename(img_path),
                        "bank_name": None,
                        "date": None,
                        "payee_name": None,
                        "amount_numeric": None,
                        "amount_words": None,
                        "cheque_number": None,
                        "account_number": None,
                        "ifsc_code": None,
                        "micr_code": None,
                        "signature_present": None,
                        "is_valid": False,
                        "confidence_score": 0,
                        "confidence_level": "Low",
                        "error_flags": extracted_data.get("error")
                    }
                else:
                    validation_result = validate_cheque_data(extracted_data)
                    row = build_final_row(
                        extracted_data,
                        validation_result,
                        os.path.basename(img_path)
                    )

                all_rows.append(row)

            df = pd.DataFrame(all_rows)
            progress.progress(66)

            status.text("Step 3/3: Preparing Excel file...")
            output_excel = os.path.join(temp_dir, "cheque_output.xlsx")
            df.to_excel(output_excel, index=False)
            progress.progress(100)

            status.text("Processing completed.")

            st.subheader("Extracted Results")
            st.data_editor(df, use_container_width=True)

            st.subheader("Summary")
            st.write(f"Total cheques processed: {len(df)}")
            st.write(f"Valid cheques: {int(df['is_valid'].sum())}")
            st.write(f"Invalid cheques: {len(df) - int(df['is_valid'].sum())}")

            with open(output_excel, "rb") as f:
                st.download_button(
                    label="Download Excel File",
                    data=f,
                    file_name="cheque_output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )