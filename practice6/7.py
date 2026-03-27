a=input()
word=input().split()
m = word[0]
for i in word:
    if i > m:
        m=i
print(m)

a=int(input())
word=input().split()
m=word[0]
for i in word:
    if len(i) > len(m):
        m=i
print(m)