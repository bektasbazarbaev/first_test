import re
a=input()
def digit(z):
    return z.group()*2
x=re.sub(r"\d", digit, a)
print(x)