import re
a=input()
s=a.split("_")
x=s[0]
for i in s[1:]:
    x+= i.capitalize()
print(x)