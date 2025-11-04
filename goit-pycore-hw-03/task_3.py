import re


def normalize_phone(phone_number):
    """
    Normalizes a phone number to standard format.
    Uses regex for pattern checking inside if/elif/else.
    Adds '+38' if the international code is missing.
    """
    clean_number = re.sub("[^0-9+]", "", phone_number)
    #delete all symbols except numbers

    if re.match(r"^\+38\d+$", clean_number):
        # if it is already correct number
        return clean_number

    elif re.match(r"^380\d+$", clean_number):
        #if number start from 380 but without "+"
        return "+" + clean_number

    elif re.match(r"^0\d{9}$", clean_number):
        #if number start without code "+38"
        return "+38" + clean_number

    else:
        return "Invalid phone number"


raw_numbers = [
    "067\\t123 4567",
    "(095) 234-5678\\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)
