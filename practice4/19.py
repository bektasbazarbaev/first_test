import math

r = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

d1 = math.hypot(x1, y1)
d2 = math.hypot(x2, y2)
dist_ab = math.hypot(x1 - x2, y1 - y2)

gamma = abs(math.atan2(y1, x1) - math.atan2(y2, x2))
if gamma > math.pi: 
    gamma = 2 * math.pi - gamma

alpha1 = math.acos(r / d1)
alpha2 = math.acos(r / d2)

if alpha1 + alpha2 >= gamma:
    print(f"{dist_ab:.10f}")
else:
    l1 = math.sqrt(d1**2 - r**2)
    l2 = math.sqrt(d2**2 - r**2)
    arc = r * (gamma - alpha1 - alpha2)
    print(f"{l1 + l2 + arc:.10f}")