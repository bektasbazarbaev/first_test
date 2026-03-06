#111111111 Search
import re

txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)

#2222 findall
import re

txt = "The rain in Spain"
x = re.findall("ai", txt)
print(x)

#3333333 search
import re

txt = "The rain in Spain"
x = re.search("\s", txt)

print("The first white-space character is located in position:", x.start())

#44444
import re

txt = "The rain in Spain"
x = re.search("Portugal", txt)
print(x)
#555555555 Split
import re

txt = "The rain in Spain"
x = re.split("\s", txt)
print(x)
#6666666666
import re

txt = "The rain in Spain"
x = re.split("\s", txt, 1)
print(x)
#7777777 sub
import re

txt = "The rain in Spain"
x = re.sub("\s", "9", txt)
print(x)
#888888888 sub
import re

txt = "The rain in Spain"
x = re.sub("\s", "9", txt, 2)
print(x)
#999 SPAN
import re

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.span())
#10 string 
import re

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.string)
#11 group
import re

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.group())
