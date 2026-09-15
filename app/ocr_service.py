import re
import pytesseract
from PIL import Image


def extract_invoice_data(image_path: str):

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    invoice_number = None
    vendor_name = None
    amount = None
    tax = None

    invoice_match = re.search(
        r"Invoice\s*(?:Number|No|#)?\s*[:\-]?\s*([A-Z0-9\-]+)",
        text,
        re.IGNORECASE
    )

    amount_match = re.search(
        r"(?:Total|Amount)\s*[:\-]?\s*₹?\s*([\d,]+(?:\.\d+)?)",
        text,
        re.IGNORECASE
    )

    tax_match = re.search(
        r"Tax\s*[:\-]?\s*₹?\s*([\d,]+(?:\.\d+)?)",
        text,
        re.IGNORECASE
    )

    vendor_match = re.search(
        r"Vendor\s*[:\-]?\s*(.+)",
        text,
        re.IGNORECASE
    )

    if invoice_match:
        invoice_number = invoice_match.group(1)

    if amount_match:
        amount = float(
            amount_match.group(1).replace(",", "")
        )

    if tax_match:
        tax = float(
            tax_match.group(1).replace(",", "")
        )

    if vendor_match:
        vendor_name = vendor_match.group(1).strip()

    return {
        "invoice_number": invoice_number,
        "vendor_name": vendor_name,
        "amount": amount,
        "tax": tax,
        "raw_text": text
    }