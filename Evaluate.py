from asteval import Interpreter
aeval = Interpreter()
import pyautogui
import re
from pynput.keyboard import Controller, Key
keyboard = Controller()
from SigFigs import SigFigs

replacements = {"²":"**2", "³":"**3", "⁴":"**4", 
                "⁵": "**5","⁶":"**6", "⁷": "**7", 
                "⁸":"**8", "⁹":"**9",
                "√": "sqrt", "∛": "cbrt", " ∜": "**0.25",
                "×": "*", "^": "**", "π": "3.14159"}

unit_names = [ ' k-in', ' kip-in', ' ksi', ' kli', ' klf', ' psf', ' pli', ' kci'
               ' in4', ' lb/in', ' k/in', ' psi', ' lb-in', 'plf',
               ' in²', ' in^2', ' in³', ' in^3', ' in⁴', ' in^4',
               ' ft²', ' sf', ' lb', ' cf', ' ft³', ' ft^3', ' pcf', ' ft', ' in', ' kip']

def replace_special_characters(replacements, inp_str):
    # Replace each key in the string with its corresponding value from the dictionary
    for old, new in replacements.items():
        inp_str = inp_str.replace(old, new)
    return inp_str


def EvaluateAnywhere(input_text, eq_d):
    # Clean up input text

    #remove whitespaces and newlines
    input_text = input_text.strip()

    # remove unit names
    pattern = r'|'.join(re.escape(substring) for substring in unit_names)
    cleaned_input_text = re.sub(pattern, '', input_text)

    # Remove Anything between []
    # Any text placed between square brackets will not be evaluated
    cleaned_input_text = re.sub(r'\[.*?\]', '', cleaned_input_text)

    #Replace Special Chars:
    cleaned_input_text = replace_special_characters(replacements, cleaned_input_text)


    # CLEANING FINISHED

    # Check to see if the input text is a preDefined equation
    # if yes, type it.
    if input_text == "Directory":
        #for item in equation_dictionary.keys():
        for item in eq_d.keys():
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            keyboard.type(item)

    #elif input_text in equation_dictionary.keys():
    elif input_text in eq_d.keys():

        # if yes, press return, and type out the dictionary value
        try:
            #press return once
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            #get the dictionary value and type it.
            type_output = eq_d[input_text]
            keyboard.type(type_output)
        except:
            pass

    # If it is the name of a predefined equation, it is an equation to evaluate
    # so evaluate it
    else:
        # use asteval to evaluate the expression
        try:
            type_output = aeval(cleaned_input_text)
            # output to 4 sig figs
            type_output = sig_figs(type_output, 4)
            #Get Last Expression
            last_line = cleaned_input_text.splitlines()[-1]
            # If there are multiple variables
            if ',' in last_line:
                result = tuple(item.strip() for item in last_line.split(','))


            multi_result = type(type_output) == tuple

            # If there are multiple answers
            if multi_result:
                # Grab the variables from the LAST LINE and make them into a tuple
                variables = tuple(item.strip() for item in last_line.split(','))

                #delete the multi-line
                pyautogui.keyDown('shift')
                pyautogui.press('home')
                pyautogui.keyUp('shift')
                # iterate through the variables tuple and results tuple
                # and print
                for i in range(len(type_output)):
                    result = str(type_output[i])
                    keyboard.type(variables[i]+" = " + result)
                    # new line after printing
                    pyautogui.press('enter')


            # if there's just one answer
            else:
                type_output = str(type_output)
                keyboard.type(" = "+type_output)
        except:
            pass