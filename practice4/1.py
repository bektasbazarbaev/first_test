
def squa(a):
    for i in range(1, a+1):
        yield i*i  
a = int(input())
for ind in squa(a):
    print(ind)