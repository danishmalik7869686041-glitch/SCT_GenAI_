\# Multimodal Visual Intelligence \& Schema Extraction



\## Project Overview

This project extracts structured information from invoice images using Gemini AI, Python, and Pydantic. It validates extracted fields and flags unreadable information for manual review.



\## Features

\- Extract invoice dates, currencies, totals, and line items from images.

\- Validate structured output using Pydantic.

\- Detect missing or unreadable fields.

\- Flag low-confidence results for manual review.

\- Provide a Flask web interface for uploading invoice images.



\## Technologies Used

\- Python

\- Google Gemini API

\- Pydantic

\- Flask

\- Pillow



\## Test Results

\- Readable invoice: Structured data extracted and validated.

\- Blurred invoice: Unreadable fields flagged for manual review.



\## Run Locally

1\. Install dependencies using `pip install -r requirements.txt`.

2\. Add your Gemini API key to a local `.env` file.

3\. Run `python web\_app.py`.

4\. Open `http://127.0.0.1:5000` in your browser.



\## Security

Never upload API keys or `.env` files to GitHub.



\## Internship

SkillCraft Technology — Task 03

