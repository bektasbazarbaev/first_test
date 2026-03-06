import re

txt = "Hello hello HeLLo"

print(re.findall("hello", txt))           
print(re.findall("hello", txt, re.I)) ## IGNORECASE == (re.I)