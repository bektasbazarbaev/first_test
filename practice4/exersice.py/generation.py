# Генератор функция
def squares_upto(n):
    for i in range(1, n+1):
        yield i**2  # yield береді, return емес

# Тест
N = 5
for sq in squares_upto(N):
    print(sq)

#2
def even_numbers(n):
    for i in range(n+1):
        if i % 2 == 0:
            yield i

# Пайдаланушыдан сан алу
n = int(input("Enter n: "))

# Шығару, үтірмен бөлінген түрде
print(",".join(str(x) for x in even_numbers(n)))
#3
def divisible_by_3_and_4(n):
    for i in range(n+1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

# Тест
n = 50
for num in divisible_by_3_and_4(n):
    print(num, end=" ")

#4
def squares(a, b):
    for i in range(a, b+1):
        yield i**2

# Тест
for value in squares(3, 7):
    print(value)

#5
def countdown(n):
    for i in range(n, -1, -1):  # n..0
        yield i

# Тест
for num in countdown(5):
    print(num)