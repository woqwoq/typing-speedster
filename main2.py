import json

code_file = open('dicts/Code.txt.concept', 'r')

json_text = json.load(code_file)

json_text.append({'entry_number' : '3', 'entry_text' : 'asf\nff'}) 

print(json_text)