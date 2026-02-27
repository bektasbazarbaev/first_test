def countdown(n):
    for i in range(n, -1, -1):  # от n до 0 включительно
        yield i

n = int(input())

for num in countdown(n):
    print(num)