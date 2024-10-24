import re
import dateparser

def text_to_cron(text):
    text = text.lower().strip()  
    cron_expression = ""

    days_of_week = {
        "sunday": 0,
        "monday": 1,
        "tuesday": 2,
        "wednesday": 3,
        "thursday": 4,
        "friday": 5,
        "saturday": 6
    }

    monthly_pattern = re.search(r'at (\d{1,2}:\d{2} (am|pm|noon|midnight))?,? on day (\d{1,2})', text)
    if monthly_pattern:
        time_part = monthly_pattern.group(1) if monthly_pattern.group(1) else "midnight" 
        hour, minute = parse_time(time_part)
        day = monthly_pattern.group(3)
        cron_expression = f"{minute} {hour} {day} * *"
        return cron_expression

    if "every day" in text or "daily" in text:
        time_part = extract_time(text)
        hour, minute = parse_time(time_part)
        cron_expression = f"{minute} {hour} * * *"

    
    else:
        matched = False
        for day, cron_day in days_of_week.items():
            if f"every {day}" in text or f"on {day}" in text:
                time_part = extract_time(text)
                hour, minute = parse_time(time_part) if time_part else (0, 0)  
                cron_expression = f"{minute} {hour} * * {cron_day}"
                matched = True
                break  
        if not matched:
            if "every hour" in text:
                cron_expression = "0 * * * *" 
            elif "every minute" in text:
                cron_expression = "* * * * *"  
            else:
                return "Invalid pattern"

    return cron_expression


def extract_time(text):
    """Extract the time part from the text."""
    time_pattern = re.search(r'at (\d{1,2}(:\d{2})? (am|pm|noon|midnight))', text)
    if time_pattern:
        return time_pattern.group(1)
    return ""  

def parse_time(time_str):
    """Helper function to parse time like '8 AM', 'noon', or 'midnight'."""
    if not time_str:
        return 0, 0  
    time_obj = dateparser.parse(time_str)
    if time_obj:
        return time_obj.hour, time_obj.minute

    return 0, 0  

text_samples = [
    "every day at 8 AM",
    "every Monday",
    "every hour",
    "every minute",
    "every Wednesday at 3:15 PM",
    "every Saturday at noon",
    "every day at midnight",
    "on Tuesday at 10:30 AM",
    "every Friday at noon",
    "on Thursday at midnight",
    "At 12:00 AM, on day 1 of the month",
    "At 12:00 AM, only on Friday"
]

for text in text_samples:
    cron_expression = text_to_cron(text)
    print(f"'{text}' => '{cron_expression}'")
