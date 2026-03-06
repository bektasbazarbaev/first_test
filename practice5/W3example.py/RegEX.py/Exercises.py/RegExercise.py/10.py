import re

s = input()
s_snake = re.sub(r'(?<!^)([A-Z])', r'_\1', s)
s_snake = s_snake.lower()

print(s_snake)