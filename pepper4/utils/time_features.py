from datetime import datetime, time

def is_active_between_hours(start_hour, end_hour, tz=None):
    now = datetime.now(tz).time() if tz else datetime.now().time()
    return time(start_hour) <= now <= time(end_hour)

def is_active_on_days(days):
    # days: list of integers, 0=Monday, 6=Sunday
    today = datetime.now().weekday()
    return today in days

def get_daily_offer(offers):
    today = datetime.now().date()
    idx = today.toordinal() % len(offers)
    return offers[idx]

def is_campaign_active(start_dt, end_dt, tz=None):
    now = datetime.now(tz) if tz else datetime.now()
    return start_dt <= now <= end_dt
