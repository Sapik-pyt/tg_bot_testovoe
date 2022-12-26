import datetime
import re


def validate_phone_number(number: str) -> bool:
    number = number.replace('+', '')
    if len(number) == 11 and number.isdigit() and number[0] in ('7', '8'):
        return True
    return False


def validate_name(name: str) -> bool:
    if name != '' and name.isalpha():
        return True
    return False


def validate_email(email: str) -> bool:
    email_regex = re.compile(
        r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
    )
    if email_regex.match(email):
        return True
    return False


def validate_birth_day(date: int) -> bool:
    if datetime.datetime.strptime(date, '%d.%m.%Y'):
        return True
    return False
