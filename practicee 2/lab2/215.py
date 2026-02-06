a=int(input())

names=set()

for i in range(a):
    surname = input().strip()
    if surname not in names:
        names.add(surname)
print(len(names))