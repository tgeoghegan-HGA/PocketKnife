

from pynput import keyboard
import pandas as pd
import pyautogui
import time
import pyperclip
from Evaluate import Evaluate
from asteval import Interpreter
from Lookup import Lookup
from Tesseract import ImageToText
aeval = Interpreter()
from GrabHighlightedText import GrabHighlightedText
from GrabGoogleSheet import GrabGoogleSheet
from Measurer import Measurer
#from Measurer import Measurer

#Define Excel File
xl_file = 'PocketKnife.xlsx'

# create dictionary for calcs
calc_df = pd.read_excel(xl_file, sheet_name='Dictionary')
calc_df = calc_df.dropna(axis=1, how='all')
calc_dict = dict(zip(calc_df['key'], calc_df['value']))

# create dictionary for lookupexamples
lookup_df = pd.read_excel(xl_file, sheet_name='Lookup')
lookup_df = lookup_df.dropna(axis=1, how='all')
lookup_examples_dict = dict(zip(lookup_df['key'], lookup_df['value']))

# Try to Grab Google sheet data and place it into a dataframe
loc = "https://docs.google.com/spreadsheets/d/1mSEJtzy5L0nuIMRlY9rYdC5s899Ptu2gdMJcIalr5pg/edit#gid=1606352415"
# Replace with your modified URL
url = "https://docs.google.com/spreadsheets/d/1I_Bih_G4gx1wPw7Hv7ENS-OwPCKoPhm5IigsyaioPyE/edit?gid=0#gid=0"
new_url = GrabGoogleSheet(url)
google_df = pd.read_csv(new_url)

# Merge dataframe d and the google sheets dataframe
combined_df = pd.concat([calc_df, google_df]).drop_duplicates()
combined_df = combined_df.dropna(axis=1, how='all')
combined_dict = dict(zip(combined_df['key'], combined_df['value']))



# Here's what happens whe na button is pressed:
def on_press(key):
    try:
        if key == keyboard.Key.f10:  # Trigger on F11 key press

            # Grab the higlighted Text
            typed_input_text = GrabHighlightedText()

            # Run the highlighted text throught the SQL interpreter
            type_output = Lookup(typed_input_text, lookup_examples_dict)
            pyautogui.press('enter')
            pyautogui.typewrite(type_output)

        elif key == keyboard.Key.f11:  # Trigger on F12 key press
            # Grab the higlighted Text
            typed_input_text = GrabHighlightedText()
            Evaluate(typed_input_text, combined_dict)

        elif key == keyboard.Key.f9:  # Trigger on F9 key press
            # Grab the higlighted Text
            out_text = ImageToText()
            pyautogui.typewrite(out_text)

        elif key == keyboard.Key.f8:  # Trigger on F8 key press
            # Screengrab measurer
            out_text = Measurer()
            pyautogui.typewrite(out_text)


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