import re
import json

with open("raw.txt", encoding="utf-8") as f:
    receipt = f.read()

prices = re.findall(r'\d{1,3}(?: \d{3})*,\d{2}', receipt)
price_numbers = [float(p.replace(" ", "").replace(",", ".")) for p in prices]

quantities = re.findall(r'(\d+,\d+|\d+) x', receipt)
quantity_numbers = [float(q.replace(",", ".")) for q in quantities]

product_names = re.findall(r'\d+\.\s(.+?)\n\d', receipt, flags=re.DOTALL)

date_time_match = re.search(r'Время:\s(\d{2}\.\d{2}\.\d{4})\s(\d{2}:\d{2}:\d{2})', receipt)
date = date_time_match.group(1) if date_time_match else ""
time = date_time_match.group(2) if date_time_match else ""

payment_match = re.search(r'(Банковская карта|Наличные)', receipt)
payment_method = payment_match.group(1) if payment_match else "Неизвестно"

products = []
for name, qty, price in zip(product_names, quantity_numbers, price_numbers):
    products.append({
        "name": name.strip(),
        "quantity": qty,
        "price": price
    })

data = {
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "products": products,
    "total": sum(price_numbers)
}

print(json.dumps(data, ensure_ascii=False, indent=4))