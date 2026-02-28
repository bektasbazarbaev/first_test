
def is_leap(y):
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

days_in_month = [31,28,31,30,31,30,31,31,30,31,30,31]

def days_since_0000(y,m,d):
    days = y*365 + d
    days += sum(1 for year in range(y) if is_leap(year))
    for i in range(m-1):
        days += days_in_month[i]
        if i==1 and is_leap(y):
            days +=1
    return days

def parse(date_str):
    date, tz = date_str.split()
    y,m,d = map(int,date.split('-'))
    sign = 1 if tz[3]=='+' else -1
    hours = int(tz[4:6])
    minutes = int(tz[7:9])
    offset_days = sign*(hours*60 + minutes)/1440
    total_days = days_since_0000(y,m,d) - offset_days
    return total_days

d1 = parse(input())
d2 = parse(input())
print(int(abs(d1 - d2)))