from datetime import datetime
from typing import Optional


def get_days_from_today(date: str) -> Optional[int]:
    """
        Returns the number of days between the given date and today.
        If the given date is in the future, the result will be negative.
        If the date is invalid, returns None.
    """
    try:
        date_conversation = datetime.strptime(date, '%Y-%m-%d').date()
        current_day = datetime.today().date()
        difference = current_day - date_conversation
        return difference.days
    except ValueError:
        print("Invalid date format. Use 'YYYY-MM-DD'.")
        return None


print(get_days_from_today('2026-10-09'))
print(get_days_from_today('2021-10-09'))
print(get_days_from_today('202d-10-0f'))
