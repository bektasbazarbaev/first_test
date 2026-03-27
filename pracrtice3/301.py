a=int(input())
l=list(map(int,input().split()))
if all (i>= 0 for i in l):
    print("Yes")
else:
    print("No")