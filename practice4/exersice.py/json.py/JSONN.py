import json

# 1️⃣ JSON файлын ашу
with open("sample-data.json") as f:
    data = json.load(f)  # JSON → Python dict

# 2️⃣ 
print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':8} {'MTU':6}")
print("-" * 80)

# 3️⃣ JSON ішіндегі интерфейстерді цикл арқылы шығару
for item in data["imdata"]:
    # attributes ішінен деректерді алу
    attr = item["l1PhysIf"]["attributes"]
    
    dn = attr["dn"]
    descr = attr["descr"]          # Кейде бос болады
    speed = attr["speed"]
    mtu = attr["mtu"]
    
    # 4️⃣ Форматталған түрде print
    print(f"{dn:50} {descr:20} {speed:8} {mtu:6}")