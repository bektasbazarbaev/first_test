import re
txt = input()
p = input()
x=re.findall(p,txt)
print(len(x))