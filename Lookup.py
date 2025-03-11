from pandasql import sqldf
import pandas as pd

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

Example ='''
SELECT Label, Type, W, bf, Ix, A
FROM AISC_Table
WHERE Ix >= 80 AND TYPE = 'W'
ORDER BY W ASC
LIMIT 10
'''

def Lookup(input_text):
    if input_text == 'Lookup':
        return lookup_howto_text

    elif input_text == 'Example':
        return Example

    # If input text is in the form "Y,X", try to lookup df.loc[X][Y]
    elif input_text.count(",") == 1 and input_text.count("\n") == 0:
        input_text = input_text.strip()
        header = input_text.split(',')[0].strip()
        label = input_text.split(',')[1].strip()
        return str(df.loc[label][header])

    # Otherwise, evaluate the SQL
    else:
        type_output = sqldf(input_text)
        type_output = type_output.to_string(index=False)
        return type_output