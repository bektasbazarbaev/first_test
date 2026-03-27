file = open("demofile.txt")
x = open("demofile.txt")
#2
open("file.txt", "r")
#3
open("file.txt", "a")
#4
open("file.txt", "w")
#5
open("file.txt", "x")
#6
with open("demofile.txt") as f:
    print(f.read())
#7
with open("demofile.txt") as f:
    print(f.read(5))
#8
with open("demofile.txt") as f:
    print(f.readline())
#9
with open("demofile.txt", "a") as f:
    f.write("Now the file has more content!")
#10
with open("demofile.txt", "w") as f:
    f.write("Woops! I have deleted the content!")
#00
import os

os.mkdir("myfolder")
#11
import os

if os.path.exists("demofile.txt"):
    os.remove("demofile.txt")
else:
    print("The file does not exist")
#12
import os
os.rmdir("myfolder")
#13
import os

filename = "demofile.txt"

if os.path.exists(filename):
    os.remove(filename)
    print("File deleted")
else:
    print("File not found")
