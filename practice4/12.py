import json

def deep_diff(obj1, obj2, path=""):
    diffs = []
    # Если оба объекта словари, сравниваем ключи
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        keys = set(obj1.keys()).union(obj2.keys())
        for key in keys:
            val1 = obj1.get(key, "<missing>")
            val2 = obj2.get(key, "<missing>")
            new_path = f"{path}.{key}" if path else key
            if isinstance(val1, dict) and isinstance(val2, dict):
                diffs.extend(deep_diff(val1, val2, new_path))
            elif val1 != val2:
                diffs.append(f"{new_path} : {json.dumps(val1, separators=(',', ':'))} -> {json.dumps(val2, separators=(',', ':'))}")
    # Если один из объектов не словарь, сравниваем напрямую
    else:
        if obj1 != obj2:
            diffs.append(f"{path} : {json.dumps(obj1, separators=(',', ':'))} -> {json.dumps(obj2, separators=(',', ':'))}")
    return diffs

obj1 = json.loads(input())
obj2 = json.loads(input())

differences = deep_diff(obj1, obj2)

if differences:
    for diff in sorted(differences):
        print(diff)
else:
    print("No differences")