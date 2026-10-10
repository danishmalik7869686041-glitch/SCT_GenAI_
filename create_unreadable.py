from PIL import Image, ImageFilter

# Load the sample invoice and make its text unreadable
image = Image.open("sample_invoice.jpg").convert("RGB")
image = image.filter(ImageFilter.GaussianBlur(radius=25))
image.save("unreadable_invoice.jpg", quality=95)

print("Unreadable test image created: unreadable_invoice.jpg")
