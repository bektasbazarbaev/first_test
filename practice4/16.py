import sys
from datetime import datetime, timedelta, timezone

def get_timestamp(line):
    parts = line.split()
    date_time_str = f"{parts[0]} {parts[1]}"
    tz_str = parts[2].replace("UTC", "")
    
    sign = 1 if tz_str[0] == '+' else -1
    h_off, m_off = map(int, tz_str[1:].split(':'))
    tz = timezone(timedelta(hours=sign * h_off, minutes=sign * m_off))
    
    dt = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    dt = dt.replace(tzinfo=tz)
    return dt.timestamp()

input_data = sys.stdin.read().splitlines()
if len(input_data) >= 2:
    start_ts = get_timestamp(input_data[0])
    end_ts = get_timestamp(input_data[1])
    print(int(end_ts - start_ts))