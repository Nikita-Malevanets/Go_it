from collections import UserDict, defaultdict
from datetime import datetime, timedelta
from typing import Optional


def input_error(func):
    """
    A decorator to handle common input errors gracefully.

    Catches:
    - ValueError: For incorrect data formats (e.g., phone, date).
    - KeyError: For attempts to access a non-existent contact.
    - IndexError: For incomplete commands (e.g., "add" without a name).
    - AttributeError: For attempts to access a birthday that is not set.
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            # Pass the specific error message from the validation
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Not enough arguments. Please provide full command parameters."
        except AttributeError:
            return "Birthday not set for this contact."

    return inner


class Field:
    """Base class for all record fields (name, phone, birthday)."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    """
    Represents a phone number.
    Validates on creation that the phone number is 10 digits.
    """

    def __init__(self, value):
        if not (isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)


class Birthday(Field):
    """
    Represents a birthday.
    Validates on creation that the date is in 'DD.MM.YYYY' format.
    """

    def __init__(self, value):
        try:
            # Validate and convert string to a datetime.date object
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    """
    Represents a contact record.
    Holds a name, a list of phones, and an optional birthday.
    """

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday: Optional[Birthday] = None  # New field, optional

    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def edit_phone(self, old_number: str, new_number: str):
        found = False
        for i, phone in enumerate(self.phones):
            if phone.value == old_number:
                self.phones[i] = Phone(new_number)  # Validation happens here
                found = True
                break
        if not found:
            raise ValueError("Old phone number not found.")

    def find_phone(self, phone_number: str) -> Optional[Phone]:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday_str: str):
        self.birthday = Birthday(birthday_str)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):
    """
    A class to manage an address book, inheriting from UserDict.
    self.data is a dictionary where keys are names and values are Record objects.
    """

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError  # Handled by @input_error as "Contact not found"

    def get_upcoming_birthdays(self) -> str:
        """
        Returns a string listing users with birthdays within the next 7 days.
        Handles moving weekend birthdays to the following Monday.
        """
        today = datetime.today().date()
        # {congrats_date: [name1, name2]}
        upcoming_birthdays = defaultdict(list)

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value  # This is a date object

                # --- Logic to determine the congratulations date ---
                # 1. Calculate this year's birthday
                birthday_this_year = birthday.replace(year=today.year)

                # 2. If it has already passed, check next year
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                # 3. Calculate the difference in days
                delta_days = (birthday_this_year - today).days

                # 4. Check if it falls within our 7-day window
                if 0 <= delta_days < 7:
                    # 5. Adjust for weekends (Sat=5, Sun=6)
                    weekday = birthday_this_year.weekday()
                    if weekday == 5:  # Saturday
                        congrats_date = birthday_this_year + timedelta(days=2)
                    elif weekday == 6:  # Sunday
                        congrats_date = birthday_this_year + timedelta(days=1)
                    else:
                        congrats_date = birthday_this_year

                    # 6. Store the name by the (adjusted) congratulations date
                    upcoming_birthdays[congrats_date].append(record.name.value)

        if not upcoming_birthdays:
            return "No upcoming birthdays in the next week."

        output = []
        for congrats_date in sorted(upcoming_birthdays.keys()):
            names = ", ".join(upcoming_birthdays[congrats_date])
            # Format the date for nice output (e.g., "Monday, 13 November")
            date_str = congrats_date.strftime("%A, %d %B")
            output.append(f"{date_str}: {names}")

        return "\n".join(output)


def parse_input(user_input: str) -> tuple[str, ...]:
    """Parses user input into a command and arguments."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args: list, book: AddressBook) -> str:
    """
    Adds a new contact or updates an existing one's phone.
    Expects: [name] [phone]
    """
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        # Phone validation (10 digits) will occur in record.add_phone
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: list, book: AddressBook) -> str:
    """
    Changes an existing phone number for a contact.
    Expects: [name] [old_phone] [new_phone]
    """
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        # New phone validation will occur in record.edit_phone
        record.edit_phone(old_phone, new_phone)
        return "Contact phone changed."
    else:
        raise KeyError  # "Contact not found."


@input_error
def show_phone(args: list, book: AddressBook) -> str:
    """
    Displays the phone numbers for a given contact.
    Expects: [name]
    """
    name, *_ = args
    record = book.find(name)
    if record:
        return ", ".join(p.value for p in record.phones)
    else:
        raise KeyError  # "Contact not found."


def show_all(book: AddressBook) -> str:
    if not book.data:
        return "No contacts found."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args: list, book: AddressBook) -> str:
    """
    Adds a birthday to a contact.
    Expects: [name] [DD.MM.YYYY]
    """
    name, birthday_str, *_ = args
    record = book.find(name)
    if record:
        # Format validation (DD.MM.YYYY) will occur in record.add_birthday
        record.add_birthday(birthday_str)
        return "Birthday added."
    else:
        raise KeyError  # "Contact not found."


@input_error
def show_birthday(args: list, book: AddressBook) -> str:
    """
    Displays the birthday for a given contact.
    Expects: [name]
    """
    name, *_ = args
    record = book.find(name)
    if record:
        if record.birthday:
            return str(record.birthday)  # Uses __str__ from Birthday
        else:
            raise AttributeError  # "Birthday not set"
    else:
        raise KeyError  # "Contact not found."


def birthdays(args: list, book: AddressBook) -> str:
    """Shows upcoming birthdays for the next week."""
    return book.get_upcoming_birthdays()


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input:
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
