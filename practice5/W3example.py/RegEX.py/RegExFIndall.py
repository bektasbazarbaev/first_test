import re

txt = "apple banana cat"
x = re.findall("[a-c]", txt)
print(x)
#222
txt = "My number is 123"
x = re.findall("\d", txt)
print(x)
#333
txt = "hello hero"
x = re.findall("he..o", txt)
print(x)
#444
txt = "Hello world"
x = re.findall("world$", txt)
print(x)
#55
txt = "heeeello"
x = re.findall("he{3}llo", txt)
print(x)
#6
txt = "The rain in Spain"
x = re.findall("ai", txt)
print(x)

