import os
import json
from PIL import Image
from dotenv import load_dotenv
from google import genai

try:
    import streamlit as st
except Exception:
    st = None

load_dotenv()


def get_api_key():
    api_key = None

    if st is not None:
        try:
            api_key = st.secrets["GOOGLE_API_KEY"]
        except Exception:
            pass

    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in Streamlit secrets or .env")

    return api_key


def extract_cheque_data(original_image_path, crop_image_path=None):
    try:
        api_key = get_api_key()
        client = genai.Client(api_key=api_key)

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
            model="gemini-2.5-flash",
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

    except Exception as e:
        return {
            "error": f"Gemini API call failed: {type(e).__name__}: {str(e)}"
        }