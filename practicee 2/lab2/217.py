a=int(input())
numbers= []
for i in range(a):
    numbers.append(input().strip())

result = 0

for num in set(numbers):
    if numbers.count(num)==3:
        result += 1
print(result)