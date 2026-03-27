a=int(input())
s=list(map(int,input().split()))
summ = 0
for i in s:
    i=i*i
    summ+=i
print(summ)