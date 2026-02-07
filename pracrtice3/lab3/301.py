a=input().strip()

valid = True

for digit in a:
    if int(digit)%2 != 0:
        valid = False
        break
if valid:
        print("Valid")
else:
        print("Not valid")

