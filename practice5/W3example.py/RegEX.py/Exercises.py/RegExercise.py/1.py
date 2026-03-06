import re
a=input()
x=re.findall(r"ab*",a)
if x :
    print(x)
else:
    print("No")