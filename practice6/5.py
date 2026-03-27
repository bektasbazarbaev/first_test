a=input()
Val=False
for i in a:
    if i.lower() in ("i","e","o","u","a"):
        Val =True
        break
if Val:
    print("Yes")
else:
    print("No")

#2
a=input()
if any(i.lower in "aeiou" for i in a):
    print("Yes")
else:
    print("No")
