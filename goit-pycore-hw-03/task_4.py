from datetime import datetime, timedelta

def get_upcoming_birthdays(users):
    today = datetime.today().date()
    list_of_birthdays = []
    for user in users:
        # Convert string into a date object
        birthday = datetime.strptime(user['birthday'], '%Y.%m.%d').date()

        # Create a date for this year's birthday
        birthday_this_year = birthday.replace(year=today.year)

        # If birthday already happened this year, move it to next year
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        # Calculate how many days until the birthday
        difference = (birthday_this_year - today).days

        # include only birthdays in 0..7 days
        if 0 <= difference <= 7:
            congratulation_day = birthday_this_year

            # move to Monday if weekend
            if congratulation_day.weekday() == 5:       # Saturday
                congratulation_day += timedelta(days=2)
            elif congratulation_day.weekday() == 6:     # Sunday
                congratulation_day += timedelta(days=1)

            list_of_birthdays.append({
                "name": user['name'],
                "congratulation_day": congratulation_day.strftime("%Y.%m.%d")
            })
    return list_of_birthdays


users = [
    {"name": "John Doe", "birthday": "1985.11.09"},
    {"name": "Jane Smith", "birthday": "1990.11.08"}
]

upcoming_birthdays = get_upcoming_birthdays(users)
print("Список привітань на цьому тижні:", upcoming_birthdays)

