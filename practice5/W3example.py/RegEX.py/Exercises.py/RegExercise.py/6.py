import re
a=input()
x=re.sub(r"[ ,\.]",":",a)
if x:
    print(x)
else:
    print("no")