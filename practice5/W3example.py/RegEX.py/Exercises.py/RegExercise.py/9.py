import re

s = input()
result = re.sub(r'(?<!^)([A-Z])', r' \1', s)

print(result)