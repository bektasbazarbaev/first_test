import re
a=input()
x=re.findall(r"\d{2,}",a)
print(" ".join(x))