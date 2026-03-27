import re
a=input()
b=input()
x=re.findall(re.escape(b),a)
print(len(x))