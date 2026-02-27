import json

data = json.loads(input())
q = int(input())
queries = [input().strip() for _ in range(q)]

for query in queries:
    current = data
    found = True
    parts = query.split('.')
    for part in parts:
        while '[' in part:
            key, rest = part.split('[', 1)
            try:
                if key:
                    current = current[key]
                idx, part = rest.split(']', 1)
                current = current[int(idx)]
            except (KeyError, IndexError, TypeError, ValueError):
                found = False
                break
        if not found:
            break
        if part:
            try:
                current = current[part]
            except (KeyError, TypeError):
                found = False
                break
    if found:
        print(json.dumps(current, separators=(',', ':')))
    else:
        print("NOT_FOUND")