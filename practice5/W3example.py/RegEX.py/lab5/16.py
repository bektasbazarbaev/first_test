import re
a=input()

x=re.search(r"Name: (.*), Age: (\d+)",a)
if x:
    print(x.group(1))
    print(x.group(2))
else:
    print("No")