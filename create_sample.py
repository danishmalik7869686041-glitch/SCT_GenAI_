
from PIL import Image, ImageDraw, ImageFont

img = Image.new("RGB", (900, 650), "white")
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("arial.ttf", 25)
    title_font = ImageFont.truetype("arial.ttf", 38)
except OSError:
    font = ImageFont.load_default()
    title_font = font

draw.text((40, 30), "SAMPLE INVOICE", fill="black", font=title_font)
draw.text((40, 100), "Invoice No: INV-1001", fill="black", font=font)
draw.text((40, 150), "Date: 2026-10-10", fill="black", font=font)
draw.text((40, 200), "Item          Quantity       Amount", fill="black", font=font)
draw.text((40, 260), "Keyboard      1              INR 1250.00", fill="black", font=font)
draw.text((40, 320), "Mouse         2              INR 1000.00", fill="black", font=font)
draw.text((40, 400), "Total: INR 2250.00", fill="black", font=title_font)
draw.text((40, 500), "This is a fictional test invoice.", fill="gray", font=font)

img.save("sample_invoice.jpg", quality=95)
print("Sample invoice created successfully!")
