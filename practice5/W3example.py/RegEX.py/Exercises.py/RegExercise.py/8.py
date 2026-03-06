import re
a=input()
x=re.findall(r"[A-Z][^A-Z]*",a)
if x:
    print(x)
else:
    print("No")