import os
import json
import pandas as pd
from gemini_extract import extract_cheque_data
from validate_cheque import validate_cheque_data


def build_final_row(extracted_data, validation_result, source_file):
    row = {
        "source_file": source_file,
        "bank_name": extracted_data.get("bank_name"),
        "date": extracted_data.get("date"),
        "payee_name": extracted_data.get("payee_name"),
        "amount_numeric": extracted_data.get("amount_numeric"),
        "amount_words": extracted_data.get("amount_words"),
        "cheque_number": extracted_data.get("cheque_number"),
        "account_number": extracted_data.get("account_number"),
        "ifsc_code": extracted_data.get("ifsc_code"),
        "micr_code": extracted_data.get("micr_code"),
        "signature_present": extracted_data.get("signature_present"),
        "is_valid": validation_result.get("is_valid"),
        "confidence_score": validation_result.get("confidence_score"),
        "confidence_level": validation_result.get("confidence_level"),
        "error_flags": " | ".join(validation_result.get("errors", []))
    }
    return row


if __name__ == "__main__":
    input_folder = r"C:\Users\Saurabh\Desktop\cheque_scanner_project\processed_images"
    output_excel = r"C:\Users\Saurabh\Desktop\cheque_scanner_project\final_output_all.xlsx"

    all_rows = []

    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(".png"):
            image_path = os.path.join(input_folder, file_name)
            print(f"Processing: {file_name}")

            extracted_data = extract_cheque_data(image_path)

            if "error" in extracted_data:
                row = {
                    "source_file": file_name,
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
                row = build_final_row(extracted_data, validation_result, file_name)

            all_rows.append(row)

    df = pd.DataFrame(all_rows)
    df.to_excel(output_excel, index=False)

    print("\nExcel file created successfully:")
    print(output_excel)
    print("\nPreview:")
    print(df.to_string(index=False))