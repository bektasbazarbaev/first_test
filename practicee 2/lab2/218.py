a=int(input())
arr = []
for x in range(a):
    arr.append(input().strip())
for x in sorted(set(arr)):
    print(x,arr.index(x)+1)