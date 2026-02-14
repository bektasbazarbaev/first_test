def isUsual(num):
    for digits in [2,3,5]:
        while num % digits == 0:
            num //= digits
    return num ==1
a= int(input())
if isUsual(a):
    print("Yes")
else:
    print("No")