from datetime import datetime
import pytz

def convert_ist_to_timezone(dt_ist: datetime, timezone_str: str) -> datetime:
    ist = pytz.timezone("Asia/Kolkata")
    target_tz = pytz.timezone(timezone_str)
    return ist.localize(dt_ist).astimezone(target_tz)
