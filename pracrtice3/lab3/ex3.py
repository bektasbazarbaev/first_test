'''
n , l ,r = map(int,input().split())
san = list(map(int,input().split()))

san[l:r+1]=san[l:r+1][::-1]
print(*san)
'''
'''
a=int(input())
san=list(map(int,input().split()))
for i in range(a):
    san[i] = san[i]**2
print(*san)
'''
'''
a=int(input())

if a <= 1:
    print("NO")
else:
    for i in range (2,a):
        if a %i == 0:
            print("No")
            break
    else:
        print("YEs")
      
          '''
'''
a=int(input())
san = list(map(int,input().split()))

freq = {}

for i in san:
    if i in freq:
        freq[i] += 1
    else:
        freq[i]=1
max_freqe = 0
'''
'''
a=int(input())
names = set()

for i in range(a):
    name = input().strip()
    if name not in names:
        names.add(name)
print(len(names))
'''
'''
a=int(input())
san = list(map(int,input().split()))
sen = set()
for i in san:
    if i in sen:
        print("NO")
    else:
        print("Yes")
        sen.add(i)
'''
a=int(input())
sen = {}

for i in range(1,a+1):
    s=input().strip()
    if s not in sen:
        sen[s] = i
for x in sorted(sen):
    print(x,sen[x])