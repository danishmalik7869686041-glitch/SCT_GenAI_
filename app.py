
import os
import sys
import json
from pathlib import Path
from datetime import date
from decimal import Decimal
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError
from PIL import Image

# Load API key from .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise SystemExit(
        "GEMINI_API_KEY missing hai. Project ki .env file check karo."
    )

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
client = genai.Client(api_key=API_KEY)

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Pydantic data models
class LineItem(BaseModel):
    description: str = Field(min_length=1)
    quantity: float
    amount: Decimal


class InvoiceData(BaseModel):
    invoice_date: Optional[date] = None
    currency: Optional[str] = None
    total: Optional[Decimal] = None
    line_items: list[LineItem] = Field(default_factory=list)
    unreadable_fields: list[str] = Field(default_factory=list)
    confidence: float
    notes: list[str] = Field(default_factory=list)


PROMPT = """
You are a careful document intelligence system.
Extract information from the supplied invoice or receipt.

Return a JSON object with these fields:
- invoice_date: date in YYYY-MM-DD format, or null
- currency: three-letter ISO currency code such as INR, or null
- total: numeric total without currency symbol, or null
- line_items: list of objects containing description, quantity, amount
- unreadable_fields: list of fields that cannot be reliably read
- confidence: number from 0.0 to 1.0
- notes: list of warnings or observations

Rules:
1. Never invent missing information.
2. If a value is unclear, use null where allowed and flag it.
3. Quantity and amount must be numbers.
4. Use a lower confidence value for blurry or ambiguous text.
5. Include every readable line item.
6. Return JSON only.
"""


def extract_invoice(image_path: Path) -> dict:
    # Check and load image safely
    with Image.open(image_path) as original:
        original.verify()

    with Image.open(image_path) as original:
        if original.format not in ("JPEG", "PNG", "WEBP"):
            raise ValueError("Image JPG, PNG ya WEBP honi chahiye.")

        if original.width < 50 or original.height < 50:
            raise ValueError("Image bahut chhoti hai.")

        image = original.convert("RGB")

    # Send image to Gemini
    response = client.models.generate_content(
        model=MODEL,
        contents=[image, PROMPT],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=InvoiceData,
            temperature=0,
        ),
    )

    if not response.text:
        raise ValueError("Model ne empty response diya.")

    # Parse and validate output
    raw_data = json.loads(response.text)
    invoice = InvoiceData.model_validate(raw_data)

    # Business validation: quantities and amounts
    for index, item in enumerate(invoice.line_items):
        if item.quantity <= 0:
            invoice.unreadable_fields.append(
                f"line_items[{index}].quantity"
            )
            invoice.notes.append(
                f"Line item {index + 1} has an invalid quantity."
            )

        if item.amount < 0:
            invoice.unreadable_fields.append(
                f"line_items[{index}].amount"
            )
            invoice.notes.append(
                f"Line item {index + 1} has an invalid amount."
            )

    # Check required invoice fields
    if invoice.invoice_date is None:
        invoice.unreadable_fields.append("invoice_date")

    if invoice.currency is None:
        invoice.unreadable_fields.append("currency")

    if invoice.total is None:
        invoice.unreadable_fields.append("total")

    # Remove duplicate flags
    invoice.unreadable_fields = list(
        dict.fromkeys(invoice.unreadable_fields)
    )

    # Low-confidence warning
    if invoice.confidence < 0.75:
        invoice.notes.append(
            "Low confidence: manual review required."
        )

    if invoice.unreadable_fields:
        invoice.notes.append(
            "Some fields are missing or uncertain. "
            "Please verify the original document."
        )

    # Convert dates and decimals into JSON-compatible values
    return invoice.model_dump(mode="json")


def main():
    if len(sys.argv) < 2:
        print('Usage: python app.py "sample_invoice.jpg"')
        raise SystemExit(1)

    image_path = Path(sys.argv[1])

    if not image_path.is_absolute():
        image_path = BASE_DIR / image_path

    if not image_path.is_file():
        raise SystemExit(f"Image file nahi mili: {image_path}")

    try:
        result = extract_invoice(image_path)

        output_path = OUTPUT_DIR / "extracted_invoice.json"
        output_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        print("\n--- VALIDATED INVOICE JSON ---")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"\nJSON saved successfully: {output_path}")

        if result["unreadable_fields"]:
            print("\nREVIEW REQUIRED:")
            print(", ".join(result["unreadable_fields"]))
        else:
            print("\nNo unreadable fields were flagged.")

    except ValidationError as error:
        print("\nPydantic validation failed:")
        print(error)
        raise SystemExit(2)

    except json.JSONDecodeError:
        print("Model response valid JSON nahi tha.")
        raise SystemExit(2)

    except Exception as error:
        print(f"\nExtraction failed: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
