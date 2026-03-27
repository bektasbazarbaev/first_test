#a=int(input())
#s=list(map(int,input().split()))
#cou = 0
#for i in s:
 #   if i %2==0:
  #      cou+=1
   # else:
    #    i=i+1
#print(cou)
a=int(input())
s=list(map(int,input().split()))

evenn = list(filter(lambda x:x %2==0,s))
print(len(evenn))