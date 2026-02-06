a=int(input())
x=a
if x < 1:
    print("NO")
else:
    while x > 1:
        if x %2 !=0:
            print("NO")
            break
        x=x//2
    else:
        print("YES")