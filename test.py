from rich import text

asd = text.Text("asd")
print(len(asd))
print(type(asd))
print(type(asd[0].plain))
print(type('a'))
print(asd[0] == 'a')