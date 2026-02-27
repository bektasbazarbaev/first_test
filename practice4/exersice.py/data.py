#1
from datetime import datetime, timedelta

# 1️⃣ Бүгінгі күн
today = datetime.now()
print("Today:", today)

# 2️⃣ 5 күнді азайту
five_days_ago = today - timedelta(days=5)
print("5 days ago:", five_days_ago)

#2
from datetime import datetime, timedelta

today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:    ", today)
print("Tomorrow: ", tomorrow)
#3
from datetime import datetime

now = datetime.now()
print("Before:", now)

# microseconds-ті алып тастау
cleaned = now.replace(microsecond=0)
print("After: ", cleaned)
#4
from datetime import datetime

# Екі күн/уақыт
date1 = datetime(2026, 2, 28, 12, 0, 0)
date2 = datetime(2026, 2, 28, 14, 30, 0)

# Айырмашылық
diff = date2 - date1

# секундқа айналдыру
seconds = diff.total_seconds()
print("Difference in seconds:", seconds)