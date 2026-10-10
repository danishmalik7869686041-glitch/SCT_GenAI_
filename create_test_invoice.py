from PIL import Image, ImageDraw, ImageFont

image = Image.new("RGB", (1000, 750), "white")
draw = ImageDraw.Draw(image)

try:
    title_font = ImageFont.truetype("arial.ttf", 30)
    font = ImageFont.truetype("arial.ttf", 22)
except OSError:
    title_font = ImageFont.load_default()
    font = ImageFont.load_default()

draw.text((50, 30), "TEST INVOICE", fill="black", font=title_font)
draw.text((50, 100), "Invoice No: TEST-2048", fill="black", font=font)
draw.text((50, 145), "Invoice Date: 2026-09-18", fill="black", font=font)
draw.text((50, 190), "Currency: INR", fill="black", font=font)

draw.line((50, 245, 950, 245), fill="black", width=2)
draw.text((50, 260), "Item          Qty       Amount", fill="black", font=font)
draw.line((50, 305, 950, 305), fill="black", width=2)

draw.text((50, 325), "Notebook       3        240.00", fill="black", font=font)
draw.text((50, 375), "Pen Set        2        300.00", fill="black", font=font)
draw.text((50, 425), "USB Drive      1        450.00", fill="black", font=font)

draw.line((50, 490, 950, 490), fill="black", width=2)
draw.text((50, 525), "TOTAL: INR 990.00", fill="black", font=title_font)
draw.text((50, 600), "Fictional invoice for software testing.", fill="black", font=font)

image.save("test_invoice_2.png")
print("Created test_invoice_2.png")
