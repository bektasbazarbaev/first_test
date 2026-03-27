#1
with open("sample.txt", "w") as f:
    f.write("Hello!\n")
    f.write("This is a sample file.\n")
    f.write("Python file handling practice.")
#2
with open("sample.txt", "r") as f:
    content = f.read()
    print(content)
#3
with open("sample.txt", "a") as f:
    f.write("\nNew line added.")
with open("sample.txt") as f:
    print(f.read())
#4
import shutil

shutil.copy("sample.txt", "backup_sample.txt")
#5
import os

filename = "sample.txt"

if os.path.exists(filename):
    os.remove(filename)
    print("File deleted safely")
else:
    print("File not found")
    