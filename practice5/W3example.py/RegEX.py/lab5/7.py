import re
a=input()
p=input()
s=input()
x=re.sub(p,s,a)
if x:
    print(x)
else:
    print("no")