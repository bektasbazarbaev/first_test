import re
a=input()
txt = a
x= re.match("Hello",txt)
if x:
    print("Yes")
else:
    print("No")
