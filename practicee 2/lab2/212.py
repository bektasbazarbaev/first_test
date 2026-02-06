a=int(input())
arr=list(map(int,input().split()))

for i in range(a):
    arr[i] = arr[i]**2
print(*arr)