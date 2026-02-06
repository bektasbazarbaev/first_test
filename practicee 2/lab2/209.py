a=int(input())
arr=list(map(int,input().split()))

max_v=max(arr)
min_v=min(arr)

for i in range(a):
    if arr[i] == max_v:
        arr[i]=min_v
print(*arr)