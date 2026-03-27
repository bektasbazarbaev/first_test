#1

a=int(input())
l=list(map(int,input().split()))
sw=list(map(lambda x:x*x,l))
print(sw)
###
a=int(input())
l=list(map(int,input().split()))
sw=list(filter(lambda x:x>0,l))
print(sw)

#2
a=int(input())
from functools import reduce
num=list(map(int,input().split()))
total=reduce(lambda x,y: x+y,num)
print(total)
#3
fruits = ["apple", "banana", "cherry"]

for index, fruit in enumerate(fruits):
    print(index, fruit)
##
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]

for name, age in zip(names, ages):
    print(name, age)
    
#4
x = "123"
print(type(x))  
y = int(x)
z = float(x)
b = str(456)
print(y, z, b)