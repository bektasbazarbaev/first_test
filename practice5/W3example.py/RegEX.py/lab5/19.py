import re
a=input()
x=re.compile(r"\b\w+\b")
z = x.findall(a)
print(len(z))