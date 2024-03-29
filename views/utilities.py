import re
from datetime import datetime

from config import DATE_FORMAT


def validate_non_empty(input_string):
    """Check that the field is not empty."""
    return bool(input_string.strip())


def validate_email(email):
    """Validate the email format."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def enforce_max_length(value, max_length):
    if len(value) > max_length:
        return False  # Reject the character
    else:
        return True


def validate_password_strength(password):
    """Validate password strength and return a tuple indicating success and a message."""
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"\W", password) is None

    if (
        length_error
        or digit_error
        or uppercase_error
        or lowercase_error
        or symbol_error
    ):
        message = "Password must be at least 8 characters long, include a mix of upper and lower case letters, have at least one number, and one special character."
        return False, message
    else:
        return True, "Password is strong."


def validate_and_convert_date(date_str):
    """Validate the date format and convert to a date object."""
    is_valid_date, message = validate_date(date_str)
    if not is_valid_date:
        return None, message  # Return early if the date format is invalid

    try:
        date_obj = datetime.strptime(date_str, DATE_FORMAT).date()
        return date_obj, "Date is valid."
    except ValueError as e:
        return None, f"Date conversion error: {e}"


def validate_date(date_str):
    """Validate date format YYYY-MM-DD and return boolean status and message."""
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return True, "Valid date."
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD."
