from zoneinfo import ZoneInfo
from datetime import datetime

def now():
    return datetime.now(tz=ZoneInfo("UTC"))


def today():
    return now().date()
