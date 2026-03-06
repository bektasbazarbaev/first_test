import re
a=input()
x=re.findall(r"[A-Z][a-z]+",a)
if x:
    print(x)
else:
    print("No")