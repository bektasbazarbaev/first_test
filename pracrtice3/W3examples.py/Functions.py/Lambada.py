x = lambda a : a + 10
print(x(5))
#2'
x = lambda a, b : a * b
print(x(5, 6))
#3
x = lambda a, b, c : a + b + c
print(x(5, 6, 2))

#4
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))
#5
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)
#6
words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)