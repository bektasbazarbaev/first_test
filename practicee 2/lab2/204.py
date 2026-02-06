a=int(input())
numbers=list(map(int,input().split()))
count  = 0
for i in numbers:
    if i > 0:
        count +=1
print(count)