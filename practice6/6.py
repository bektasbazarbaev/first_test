a=int(input())
s=list(map(int,input().split()))
Val=True
for i in s:
    if i < 0:
        Val=False
        break
if Val:
    print("Yes")
else:
    print("No")