from pandasql import sqldf
import pandas as pd
from pynput.keyboard import Controller, Key
keyboard = Controller()

pd.set_option('display.max_rows', 500)
xl_path = 'PocketKnife.xlsx'
df = pd.read_excel(xl_path, 'Database v16.0' )

df = df.rename(columns={'AISC_Manual_Label': 'Label'})

df = df.set_index('Label')
AISC_Table = df.copy()

lookup_howto_text = """-- There are 5 required lines in the lookup query : SELECT, FROM, WHERE, ORDER BY, LIMIT
-- Below is a quick explanation of each of them:  
-- SELECT: Add a list of desired columns
-- -- See the AISC Spreadsheet for all columns names, but a few common ones are listed below:
-- -- Label, W : Weight, D: Depth, tw : WF web thickness, tf: WF Flange Thickness, 
-- -- Ix: Moment of Intertia X axis, Type : ('W'. 'HSS', 'L', '2L', etc)
-- -- tnom: HSS-only Wall thickness, B: Width of HSS, b_ : width of flat face of HSS, Ht: Height of HSS
-- -- h_: depth of other flat face of HSS, H: Flexural Constant, 
-- -- t_:L-angle leg thickness, T: WF web height minus fillet radii
-- -- A: Cross-Sectional Area, 
-- FROM : Just type "FROM AISC_Table" and nothing else.
-- WHERE: Use the following operators to filter the table:
-- -- >, >=, =, AND, OR, NOT
-- -- Types: W, M, S, HP, C, MC, L, WT, MT, ST, 2L, HSS, HSSRND, PIPE 
-- ORDER BY : Choose the column by which the results will be sorted
-- LIMIT : How many results do you want?

SELECT Label, Type, W, bf, Ix, A
FROM AISC_Table
WHERE Ix >= 80 AND TYPE = 'W'
ORDER BY W ASC
LIMIT 5
"""



New_Example = '''
COLUMNS: Label, Type, W, bf, Ix, A
WHERE: Ix >= 80 AND TYPE = 'W'
ORDER: BY W
LIMIT: 10
'''

def Lookup(input_text, lookup_dict):
    if input_text == 'Lookup':
        return lookup_howto_text

    elif input_text == "Directory":
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