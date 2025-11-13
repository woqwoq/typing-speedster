code_lines = open("dicts/Code.txt", 'r').readlines()
code_lines = ''.join(code_lines).replace('    ', '\t').split('---')

res_lines = []
for i in range(len(code_lines)):
    code_lines[i] = code_lines[i].strip('\n')
    if(code_lines[i] != ''):
        res_lines.append(code_lines[i])


print(res_lines)