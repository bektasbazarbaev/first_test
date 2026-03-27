a=int(input())
keys=input().split()
val=input().split()
dic=dict(zip(keys,val))
w=input()
if w in dic:
    print(dic[w])
else:
    print("Not found")