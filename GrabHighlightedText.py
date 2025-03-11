import pyperclip
import time
from pynput import keyboard


def GrabHighlightedText():
    # Simulate Ctrl+C to copy selected text to clipboard
    controller = keyboard.Controller()
    controller.press(keyboard.Key.ctrl)
    controller.press('c')
    controller.release('c')
    controller.release(keyboard.Key.ctrl)

    # Give time for the clipboard to update
    time.sleep(0.1)

    # Reprint the selected_texxt
    typed_input_text = pyperclip.paste()

    controller.press((keyboard.Key.right))

    return typed_input_text