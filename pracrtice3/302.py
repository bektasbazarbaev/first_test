a=int(input())
l=list(map(int,input().split()))
ls=sum(map(lambda x: x>0,l))
print(ls)