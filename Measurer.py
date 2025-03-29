from PIL import ImageGrab, Image
import math

def Measurer():
    """Returns the size (width, height) of an image stored in the clipboard."""
    try:
        image = ImageGrab.grabclipboard()
        if isinstance(image, Image.Image):
           # return image.size  # Returns (width, height)
            height = image.size[1]
            width = image.size[0]
            text = ""
            text += "height = " + str(height)
            text += "\n"
            text += "width = " + str(width)
            text += "\n"
            text += "area = " + str(width * height)
            text += "\n"
            text += "rise/run = " + str(round(height/width, 3))
            text += "\n"
            text += "angle = " + str(round(math.degrees(math.atan(height/width)),2))

            return text
        else:
            return None  # No image found in clipboard
    except Exception as e:
        return f"Error: {e}"