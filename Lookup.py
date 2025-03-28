from pandasql import sqldf
import pandas as pd
from pynput.keyboard import Controller, Key
keyboard = Controller()

pd.set_option('display.max_rows', 500)
xl_path = 'PocketKnife.xlsx'
df = pd.read_excel(xl_path, 'Database v16.0' )

df = df.rename(columns={'AISC_Manual_Label': 'Label'})

df = df.set_index('Label')

New_Example = '''
COLUMNS: Label, Type, W, bf, Ix, A
WHERE: Ix >= 80 AND TYPE = 'W'
ORDER: BY W
LIMIT: 10
'''

def Lookup(input_text, lookup_dict):

    if input_text == "Directory":
        print("looking up")
        # If yes, print all items in the dictionary
        for item in lookup_dict.keys():
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            keyboard.type(item)


    # If input text is in the form "Y,X", try to lookup df.loc[X][Y]
    elif input_text.count(",") == 1 and input_text.count("\n") == 0:
        input_text = input_text.strip()
        header = input_text.split(',')[0].strip()
        label = input_text.split(',')[1].strip()
        return str(df.loc[label][header])
    
    # Check to see if the input text is a preDefined dictionary key

    elif input_text in lookup_dict.keys():

        # if yes, press return, and type out the dictionary value
        try:
            #press return once
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            #get the dictionary value and type it.
            type_output = lookup_dict[input_text]
            keyboard.type(type_output)
        except:
            pass
    # Otherwise, evaluate the SQL
    else:
        # 1 Strip the input text
        input_text = input_text.strip()
        # 2 Remove all ":"
        input_text = input_text.replace(":", "")
        # 3 Replace "COLUMNS" with "SELECT"
        input_text = input_text.replace("COLUMNS", "SELECT")
        input_text_list = input_text.split("\n")
        j = input_text_list.pop(1)

        input_text_list.insert(1,j)
        input_text_list.insert(1,"FROM df")

        input_text = ""
        for item in input_text_list:
            input_text += item
            input_text += "\n"

        type_output = sqldf(input_text)
        type_output = type_output.to_string(index=False)
        return type_output