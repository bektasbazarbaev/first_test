a=int(input())
arr1=list(map(int,input().split()))
arr2=list(map(int,input().split()))
cou = 0
for i in range(a):
    m=arr1[i]*arr2[i]
    cou += m
print(cou)