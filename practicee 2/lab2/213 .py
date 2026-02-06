a=int(input())

if a <= 1:
    print("No")
else:
    is_prime = True
    for i in range(2,a):
        if a % i == 0:
            is_prime = False
            break
    if is_prime:
        print("Yes")

    else:
        print("No")
        