
#1
import os

os.makedirs("project/data/files")
#2
import os

items = os.listdir("project")
print(items)
#3
import os

for file in os.listdir("project"):
    if file.endswith(".txt"):
        print(file)
#4
import shutil
shutil.copy("sample.txt", "project/sample.txt")
shutil.move("sample.txt", "project/sample.txt")