  # 1 Strip the input text

input_text = '''
COLUMNS: Label, Type, W, bf, Ix, A
WHERE: Ix >= 80 AND TYPE = 'W'
ORDER: BY W
LIMIT: 10
'''
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

print(input_text)