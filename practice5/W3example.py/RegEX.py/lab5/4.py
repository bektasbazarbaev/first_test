import re
a=input()

x=re.findall(r"\d",a)
if x:
    print(" ".join(x))
else:
    None