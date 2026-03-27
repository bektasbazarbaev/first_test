#a=int(input())
#word=input().split()
#for i in range(a):
#    print(f"{i}:{word[i]}",end=" ")
a=int(input())
word = input().split()
for index,words in enumerate(word):
    print(f"{index}:{words}",end=" ")