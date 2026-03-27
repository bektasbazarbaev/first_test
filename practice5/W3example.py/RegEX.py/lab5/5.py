import re
a=input()
x=re.findall(r"^[a-zA-Z].*\d$",a)
if x:
    print("Yes")
else:
    print("No")