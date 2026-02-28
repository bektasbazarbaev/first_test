from datetime import datetime, timedelta, timezone

def solve():
    try:
        line1 = input().split()
        line2 = input().split()
    except EOFError:
        return

    def get_seconds(date_str, tz_str, override_year=None):
        y, m, d = map(int, date_str.split('-'))
        if override_year:
            y = override_year
            if m == 2 and d == 29:
                is_leap = (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0))
                if not is_leap:
                    d = 28
        
        offset = tz_str.replace("UTC", "")
        sign = 1 if offset[0] == '+' else -1
        h, m_off = map(int, offset[1:].split(':'))
        tz = timezone(timedelta(hours=sign*h, minutes=sign*m_off))
        
        dt = datetime(y, m, d, tzinfo=tz)
        return dt.timestamp()

    t_now = get_seconds(line2[0], line2[1])
    
    b_date_raw = line1[0]
    b_tz_raw = line1[1]
    curr_year = int(line2[0].split('-')[0])

    t_bday = get_seconds(b_date_raw, b_tz_raw, curr_year)
    
    if t_bday < t_now:
        t_bday = get_seconds(b_date_raw, b_tz_raw, curr_year + 1)
    
    delta = t_bday - t_now
    
    if delta <= 0:
        print(0)
    else:
        print(int((delta + 86399) // 86400))

solve()