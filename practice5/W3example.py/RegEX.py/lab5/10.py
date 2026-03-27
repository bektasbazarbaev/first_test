import re
a=input()
x=re.findall(r"cat|dog",a)
if x:
    print("Yes")
else:
    print("No")