import re
a=input()

x=re.findall(r"[a-z]+_[a-z]+",a)
if x:
    print(x)
else:
    print("No")