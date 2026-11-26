import datetime
import pytz

def is_local_business_hours(country_code: str = "IN") -> bool:
    """Checks if current local time in target country is within professional office hours (9 AM - 6 PM)."""
    try:
        if country_code.upper() == "US":
            tz = pytz.timezone("America/New_York")
        elif country_code.upper() == "GB" or country_code.upper() == "UK":
            tz = pytz.timezone("Europe/London")
        elif country_code.upper() == "AE" or country_code.upper() == "DXB":
            tz = pytz.timezone("Asia/Dubai")
        else:
            tz = pytz.timezone("Asia/Kolkata") # Default India

        local_now = datetime.datetime.now(tz)
        hour = local_now.hour
        weekday = local_now.weekday() # 0 to 6 (Mon-Sun)

        # Professional office hours: Monday to Saturday, 9 AM to 7 PM
        if weekday <= 5 and 9 <= hour < 19:
            return True
        return False
    except Exception:
        # Fallback if pytz is missing or error
        now_hour = datetime.datetime.now().hour
        return 9 <= now_hour < 19

def get_next_business_hour_delay(country_code: str = "IN") -> int:
    """Returns seconds to sleep if it is outside office hours, or 0 if inside."""
    if is_local_business_hours(country_code):
        return 0
    # If outside office hours, sleep for a safe interval or queue for daytime dispatch
    return 3600 # 1 hour check interval
