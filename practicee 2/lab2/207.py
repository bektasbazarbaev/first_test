a=int(input())
numbers=list(map(int,input().split()))
num = -1e9
index = 0
for i,val in enumerate(numbers):
    if val > num:
        num = val
        index = i
print(index+1)