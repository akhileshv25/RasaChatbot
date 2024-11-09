import re
from datetime import datetime, timedelta

def extract_start_time_millis(recurrence_rule):
    time_pattern = r'(\d{1,2}(:\d{2})?\s?(am|pm|AM|PM)?)'
    time_match = re.search(time_pattern, recurrence_rule)
    
    if time_match:
        time_str = time_match.group(1).strip()
        
        try:
            start_time = datetime.strptime(time_str, "%I %p").time()
        except ValueError:
            try:
                start_time = datetime.strptime(time_str, "%H:%M").time()
            except ValueError:
                start_time = datetime.strptime(time_str, "%H").time()

        current_date = datetime.today()
        start_datetime = datetime.combine(current_date, start_time)
        
        millis_since_epoch = int(start_datetime.timestamp() * 1000)
        
        return millis_since_epoch
    else:
        return None

recurrence_rule = "7 pm every Sunday"
start_time_millis = extract_start_time_millis(recurrence_rule)

if start_time_millis is not None:
    print("Start time in milliseconds since Unix epoch:", start_time_millis)
else:
    print("No valid start time found in the recurrence rule.")
