a=int(input())
numbers=list(map(int,input().split()))
num = -1e9
for i in numbers:
    if i > num:
        num = i
print(num)