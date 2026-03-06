import re
a=input()
x=re.findall(r"ab{2,3}",a)
if x:
    print(x)
else:
    print("No")