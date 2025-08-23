import re


def validate_name(value: str) -> str:
    if not re.fullmatch(r'^[A-Za-z]+$', value):
        raise ValueError('Your name must contain alphabets only')
    return value.capitalize()


def validate_phone(value: str) -> str:
    if not re.fullmatch(r'^\+?[1-9]\d{7,14}$', value):
        raise ValueError('Invalid phone number format')
    return value


def validate_email(value: str) -> str:
    email_regex = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    if not re.fullmatch(email_regex, value):
        raise ValueError('Invalid email format')
    return value.lower()


def validate_password(value: str) -> str:
    if len(value) < 8:
        raise ValueError('Password must be at least 8 characters long')
    if not re.search(r'[A-Z]', value):
        raise ValueError('Password must contain at least one uppercase letter')
    if not re.search(r'[a-z]', value):
        raise ValueError('Password must contain at least one lowercase letter')
    if not re.search(r'\d', value):
        raise ValueError('Password must contain at least one number')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValueError('Password must contain at least one special character')
    return value

