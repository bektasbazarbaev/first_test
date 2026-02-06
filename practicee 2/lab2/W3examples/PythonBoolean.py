a = 200
b = 33

if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

# 2:
print(bool("Hello"))
print(bool(15))

#3
x = "Hello"
y = 15

print(bool(x))
print(bool(y))

#4
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})

#5
class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))