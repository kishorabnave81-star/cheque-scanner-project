import os
import json
from PIL import Image
from dotenv import load_dotenv
from google import genai
from validate_cheque import validate_cheque_data

try:
    import streamlit as st
except Exception:
    st = None

load_dotenv()

API_KEY = None

if st is not None:
    try:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        pass

if not API_KEY:
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in Streamlit secrets or .env")

client = genai.Client(api_key=API_KEY)


def extract_cheque_data(original_image_path, crop_image_path=None):
    original_img = Image.open(original_image_path)

    prompt = """
You are a cheque data extraction system.

Extract cheque information from the provided image(s) and return ONLY valid JSON.

Rules:
- Return JSON only
- No explanation
- No markdown
- If a field is missing, use null
- Keep field names exactly as given below

Required JSON format:
{
  "bank_name": null,
  "date": null,
  "payee_name": null,
  "amount_numeric": null,
  "amount_words": null,
  "cheque_number": null,
  "account_number": null,
  "ifsc_code": null,
  "micr_code": null,
  "signature_present": null
}
"""

    contents = [prompt, original_img]

    if crop_image_path and os.path.exists(crop_image_path):
        crop_img = Image.open(crop_image_path)
        contents.append(crop_img)

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=contents
    )

    raw_text = response.text.strip()

    try:
        data = json.loads(raw_text)
        return data
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by Gemini",
            "raw_output": raw_text
        }


if __name__ == "__main__":
    original_path = r"C:\Users\Saurabh\Desktop\cheque_scanner_project\processed_images\page_1.png"
    crop_path = None

    extracted_data = extract_cheque_data(original_path, crop_path)
    print("EXTRACTED DATA:")
    print(json.dumps(extracted_data, indent=4))

    if "error" not in extracted_data:
        validation_result = validate_cheque_data(extracted_data)
        print("\nVALIDATION RESULT:")
        print(json.dumps(validation_result, indent=4))
    else:
        print("\nVALIDATION SKIPPED DUE TO EXTRACTION ERROR")
