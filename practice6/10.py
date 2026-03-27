"""
a=int(input())
s=list(map(int,input().split()))
cou=0

n = True

for i in s:
    if i ==0:
        n=False
    else:
        cou +=1
#if n:
 #   print(cou)
"""
#1
"""
a=int(input())
s=list(map(int,input().split()))
res=map(lambda x: x*x,s)
resel=sum(res)
print(resel)
"""
#2
"""
a=int(input())
s=list(map(int,input().split()))
res=list(filter(lambda x: x%2 ==0, s))
print(len(res))
"""
#3
"""
a=int(input())
words=input().split()
for i,w in enumerate(words):
    print(f"{i}:{w}",end=" ")
"""
#4
"""
a=int(input())
ar1=list(map(int,input().split()))
ar2=list(map(int,input().split()))
res=0
for x1,x2 in zip(ar1,ar2):
    res += x1*x2
print(res)
"""
#5
"""
a=input()
if any(r in "aeoui" for r in a.lower()):
    print("Yes")
else:
    print("No")
    """
#6
"""
a=int(input())
s=list(map(int,input().split()))
if all(r >=0 for r in s):
    print("Yes")
else:
    print("No")
"""
#7
"""
a=int(input())
words=input().split()
res=max(words,key=len)
print(res)
"""