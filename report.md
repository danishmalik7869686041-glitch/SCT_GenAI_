**# Multimodal Visual Intelligence \& Schema Extraction**



**## Objective**

**Build a Python-based document intelligence pipeline that extracts structured information from invoice images using a vision-enabled Gemini model.**



**## Technologies Used**

**- Python**

**- Google Gemini API**

**- Pydantic**

**- Pillow**

**- python-dotenv**



**## Pipeline**

**1. Load an invoice image.**

**2. Send the image to the Gemini vision model.**

**3. Extract invoice date, currency, total, and line items.**

**4. Validate the response using Pydantic models.**

**5. Flag missing or unreadable fields and low-confidence results.**

**6. Save the validated JSON output.**



**## Test Case 1: Sample Invoice**



**\*\*Input:\*\* `sample\_invoice.jpg`**



**\*\*Expected invoice total:\*\* INR 2250.00**



**\*\*Observed output:\*\***

**- Invoice date: 2026-10-10**

**- Currency: INR**

**- Total: 2250.0**

**- Line items: Keyboard and Mouse**

**- Unreadable fields: None**

**- Model-reported confidence: 1.0**



**\*\*Result:\*\* Passed for the sample invoice.**



**## Validation and Limitations**

**Pydantic validates the structure and data types. Additional application checks flag non-positive quantities and negative amounts. Missing required invoice fields are flagged for review.**



**The confidence value is estimated by the vision model and is not a calibrated probability. Extracted values should be verified against the original document before real-world use.**



**## Deliverables**

**- `app.py` — extraction and validation pipeline**

**- `create\_sample.py` — sample invoice generator**

**- `sample\_invoice.jpg` — test input**

**- `outputs/extracted\_invoice.json` — validated output**

**- `report.md` — project report**

**- `requirements.txt` — Python dependencies**

**## Test Case 2: Blurred / Unreadable Invoice**



**\*\*Input:\*\* `unreadable\_invoice.jpg`**



**\*\*Test method:\*\* Applied a strong Gaussian blur to the sample invoice.**



**\*\*Observed output:\*\***

**- Invoice date: null**

**- Currency: null**

**- Total: null**

**- Line items: empty**

**- Unreadable fields: invoice\_date, currency, total, line\_items**

**- Model-reported confidence: 0.0**

**- Review status: Manual review required**



**\*\*Result:\*\* Passed. The model identified the image as illegible, returned null for unavailable fields, and flagged the document for manual review.**



**## Overall Testing Summary**



**| Test case | Expected behavior | Result |**

**|---|---|---|**

**| Readable invoice | Extract structured invoice data | Passed |**

**| Blurred invoice | Flag unreadable fields for review | Passed |**



**Both tests passed for the tested sample inputs. Further testing with different invoice layouts and image quality is recommended.**



