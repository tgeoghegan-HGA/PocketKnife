from PIL import Image, ImageGrab
import pytesseract
from sympy import sympify

pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR\\tesseract.exe"
def ImageToText():
    image = ImageGrab.grabclipboard()

    if isinstance(image, Image.Image):  # Ensure clipboard contains an image
        text = pytesseract.image_to_string(image)
        print("Extracted Text:\n", text)
        return text
    else:
        print("No image found in clipboard.")