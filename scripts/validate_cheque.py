import re
import json


def validate_date(date_str):
    if not date_str:
        return False
    pattern = r"^\d{2}/\d{2}/\d{4}$"
    return bool(re.match(pattern, date_str))


def validate_cheque_number(cheque_number):
    if not cheque_number:
        return False
    cheque_number = str(cheque_number).strip()
    return cheque_number.isdigit() and 6 <= len(cheque_number) <= 10


def validate_ifsc(ifsc_code):
    if not ifsc_code:
        return False
    pattern = r"^[A-Z]{4}0[A-Z0-9]{6}$"
    return bool(re.match(pattern, ifsc_code))


def validate_micr(micr_code):
    if not micr_code:
        return False
    micr_code = str(micr_code).strip()
    return micr_code.isdigit() and len(micr_code) == 9


def validate_signature(signature_present):
    return isinstance(signature_present, bool)


def words_to_number_indian(words):
    if not words:
        return None

    words = words.lower().replace("only", "").strip()

    number_words = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
        "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
        "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
        "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90
    }

    multipliers = {
        "hundred": 100,
        "thousand": 1000,
        "lakh": 100000,
        "crore": 10000000
    }

    tokens = words.replace("-", " ").split()
    total = 0
    current = 0

    for token in tokens:
        if token in number_words:
            current += number_words[token]
        elif token == "hundred":
            current *= 100
        elif token in ["thousand", "lakh", "crore"]:
            current *= multipliers[token]
            total += current
            current = 0

    total += current
    return total if total > 0 else None


def validate_amount_match(amount_numeric, amount_words):
    if not amount_numeric or not amount_words:
        return False

    try:
        numeric_value = int(str(amount_numeric).replace(",", "").strip())
    except:
        return False

    words_value = words_to_number_indian(amount_words)

    if words_value is None:
        return False

    return numeric_value == words_value


def validate_required_fields(data):
    required_fields = [
        "bank_name",
        "date",
        "payee_name",
        "amount_numeric",
        "amount_words",
        "cheque_number",
        "account_number",
        "ifsc_code",
        "micr_code",
        "signature_present"
    ]

    missing = []
    for field in required_fields:
        if field not in data or data[field] in [None, ""]:
            missing.append(field)
    return missing


def validate_cheque_data(data):
    errors = []

    if not validate_date(data.get("date")):
        errors.append("Invalid date format")

    if not validate_cheque_number(data.get("cheque_number")):
        errors.append("Invalid cheque number")

    if not validate_ifsc(data.get("ifsc_code")):
        errors.append("Invalid IFSC code")

    if not validate_micr(data.get("micr_code")):
        errors.append("Invalid MICR code")

    if not validate_signature(data.get("signature_present")):
        errors.append("Invalid signature flag")

    if not validate_amount_match(data.get("amount_numeric"), data.get("amount_words")):
        errors.append("Amount words and numeric amount do not match")

    missing_fields = validate_required_fields(data)
    if missing_fields:
        errors.append(f"Missing fields: {', '.join(missing_fields)}")

    score = 100 - (len(errors) * 15)
    if score < 0:
        score = 0

    if score >= 80:
        confidence = "High"
    elif score >= 50:
        confidence = "Medium"
    else:
        confidence = "Low"

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "confidence_score": score,
        "confidence_level": confidence
    }


if __name__ == "__main__":
    sample_data = {
        "bank_name": "ICICI Bank",
        "date": "09/02/2016",
        "payee_name": "B. Shiva Kumar",
        "amount_numeric": "1400000",
        "amount_words": "Two crore four lakh",
        "cheque_number": "100830",
        "account_number": "630601501452",
        "ifsc_code": "ICIC0006306",
        "micr_code": "500229009",
        "signature_present": True
    }

    result = validate_cheque_data(sample_data)
    print(json.dumps(result, indent=4))