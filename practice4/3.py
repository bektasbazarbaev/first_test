n = int(input())

first = True
for i in range(0, n + 1):
    if i % 12 == 0:
        if first:
            print(i, end="")
            first = False
        else:
            print(" ", i, end="")
print()