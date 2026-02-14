'''
a=int(input())
if a % 4 == 0 and a % 100 != 0 or a % 400 == 0:
    print("YES")
else:
    print("NO")
'''
'''
a=int(input())
res = sum(range(1,a+1))
print(res)
'''
'''
a=int(input())
sha=input().split()

total = 0
for element in range(a):
    total += int(sha[element])

print(total)
'''
'''
a=int(input())
sha=input().split()

sum = 0
for i in range(a):
    if int(sha[i]) > 0:
        sum+= 1
print(sum)
'''
'''
a=int(input())
while a != 1:
    if a %2 == 0:
        a//= 2
    else:
        print("NO")
        break
else:
    print("YES")
'''
'''
a=int(input())
shy= input().split()

san=[]
for i in range(a):
    san.append(int(shy[i]))
print(max(san))
'''
'''
a=int(input())
shy=input().split()
san=[]
for i in range(a):
    san.append(int(shy[i]))
mink = int(-1e9)
index = 0
for i in range(a):
    if san[i] > mink:
        mink = san[i]
        index = i
print(index+1)
'''
'''
a=int(input())

b= 1
while b <= a:
    print(b,end =" ")
    b *= 2
'''
'''
a=int(input())
shy = input().split()

san = []
for i in range(a):
    san.append(int(shy[i]))
mx = int(-1e9)
mn = int(1e9)
for i in range(a):
    if san[i]> mx:
        mx=san[i]
    if san[i]<mn:
        mn = san[i]
for i in range(a):
    if san[i] == mx:
        san[i] = mn
print(*san)
'''
'''
a=int(input())
shy = input().split()

san = []
for i in range(a):
    san.append(int(shy[i]))

res = sorted(san)
reste = reversed(res)
print(*reste)
'''
a=int(input())
l = int(input())
r = int(input())
shy = input().split()
san = []
for i in range(a):
    san.append(int(shy[i]))
san[l:r]
print(*san)
