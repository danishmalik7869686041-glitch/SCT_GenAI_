from flask import Flask, request, render_template_string
from pathlib import Path
import subprocess
import sys
import json

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_FILE = BASE_DIR / "outputs" / "extracted_invoice.json"

UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Invoice Intelligence</title>
<style>
body {
    font-family: Arial, sans-serif;
    background: #f3f6fb;
    color: #172033;
    max-width: 850px;
    margin: 40px auto;
    padding: 20px;
}
header, section {
    background: white;
    padding: 22px;
    border-radius: 12px;
    margin-bottom: 18px;
    box-shadow: 0 3px 12px #15213a12;
}
h1 { color: #2449a5; margin-bottom: 8px; }
p { color: #526078; }
input, button {
    padding: 12px;
    margin-top: 12px;
    max-width: 100%;
}
button {
    background: #2449a5;
    color: white;
    border: 0;
    border-radius: 7px;
    cursor: pointer;
}
pre {
    background: #101827;
    color: #d9e8ff;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}
.status { font-weight: bold; }
</style>
</head>
<body>
<header>
    <h1>Invoice Intelligence</h1>
    <p>AI-powered invoice extraction and validation</p>
</header>

<section>
    <h2>Upload Invoice</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="invoice" accept=".jpg,.jpeg,.png,.webp" required>
        <br>
        <button type="submit">Extract Invoice Data</button>
    </form>
    <p>Supported formats: JPG, PNG, WEBP</p>
</section>

{% if error %}
<section>
    <p class="status">Error: {{ error }}</p>
</section>
{% endif %}

{% if result %}
<section>
    <h2>Extraction Results</h2>
    {% if result.unreadable_fields %}
        <p class="status">Review required: Some fields are unreadable or missing.</p>
    {% else %}
        <p class="status">Extraction completed. Verify the results against the original invoice.</p>
    {% endif %}
    <pre>{{ result | tojson(indent=2) }}</pre>
</section>
{% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        uploaded = request.files.get("invoice")

        if not uploaded or not uploaded.filename:
            error = "Please choose an invoice image."
        else:
            extension = Path(uploaded.filename).suffix.lower()

            if extension not in ALLOWED_EXTENSIONS:
                error = "Unsupported file type. Upload JPG, PNG, or WEBP."
            else:
                # Use a fixed filename to avoid unsafe uploaded filenames.
                image_path = UPLOAD_DIR / f"web_upload{extension}"
                uploaded.save(image_path)

                # Run the existing extraction pipeline.
                completed = subprocess.run(
                    [sys.executable, str(BASE_DIR / "app.py"), str(image_path)],
                    cwd=str(BASE_DIR),
                    capture_output=True,
                    text=True,
                    timeout=180
                )

                if completed.returncode != 0:
                    error = "Extraction failed. Check the terminal for details."
                    print(completed.stdout)
                    print(completed.stderr)
                elif not OUTPUT_FILE.exists():
                    error = "The extraction output JSON was not created."
                else:
                    try:
                        result = json.loads(
                            OUTPUT_FILE.read_text(encoding="utf-8")
                        )
                    except (json.JSONDecodeError, OSError):
                        error = "Could not read the extraction result."

    return render_template_string(HTML, result=result, error=error)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
