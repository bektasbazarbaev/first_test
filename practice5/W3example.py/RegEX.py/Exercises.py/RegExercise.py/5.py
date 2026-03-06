import re
a=input()
x=re.search(r"a.*b",a)
if x:
    print(x.group())
else:
    print("No")