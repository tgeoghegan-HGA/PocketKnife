print("hello world")


from pynput import keyboard
import pandas as pd
import pyautogui
import time
import pyperclip
from Evaluate import Evaluate
from asteval import Interpreter
#from Lookup import Lookup
#from Tesseract import image_to_text
aeval = Interpreter()
from GrabHighlightedText import GrabHighlightedText
#from Measurer import Measurer

#Define Excel File
xl_file = 'PocketKnife.xlsx'
df = pd.read_excel(xl_file, sheet_name='Dictionary')
df = df.dropna(axis=1, how='all')
d = dict(zip(df['key'], df['value']))


# Here's what happens whe na button is pressed:
def on_press(key):
    try:
        if key == keyboard.Key.f11:  # Trigger on F11 key press

            # Grab the higlighted Text
            typed_input_text = GrabHighlightedText()

            # Run the highlighted text throught the SQL interpreter
            type_output = Lookup(typed_input_text)
            pyautogui.press('enter')
            pyautogui.typewrite(type_output)

        elif key == keyboard.Key.f12:  # Trigger on F12 key press
            # Grab the higlighted Text
            typed_input_text = GrabHighlightedText()
            Evaluate(typed_input_text, d)
            #EvaluateAnywhere(typed_input_text)

        # elif key == keyboard.Key.f9:  # Trigger on F9 key press
        #     # Grab the higlighted Text
        #     out_text = ImageToText()
        #     pyautogui.typewrite(out_text)

        # elif key == keyboard.Key.f8:  # Trigger on F8 key press
        #     # Screengrab measurer

        #     out_text = Measurer()
        #     pyautogui.typewrite(out_text)


    except Exception as e:
        print(f"Error: {e}")


def main():
    print("Listening for a Function key... Press Ctrl+C to exit.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting program.")