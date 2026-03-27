import re
a=input()

x=re.findall(r"\b\d{2}/\d{2}/\d{4}\b",a)
if x:
    print(len(x))
else:
    print("No dates")