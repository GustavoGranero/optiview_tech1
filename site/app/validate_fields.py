import re
import uuid

def is_valid_password(password):
    has_lowercase = re.search(r"[a-zç]", password) is not None 
    has_uppercase = re.search(r"[A-ZÇ]", password) is not None
    has_numbers = re.search(r"[0-9]", password) is not None 
    has_symbols = re.search(r"[!@#$%^&\*\(\)-_=+\[\]\{\}\/\|/\\\?\<\>.,~`]", password) is not None 
    return has_lowercase and has_uppercase and (has_numbers or has_symbols)

def is_valid_password_length(password):
    return len(password) >= 8

def normalize_phone(phone):
    return phone.replace(' ','').replace('-', '')

def is_valid_phone(phone):
    has_only_digits_spaces_dash = re.match(r'^[\d -]*$', phone) is not None
    is_long_enough = len(normalize_phone(phone)) >= 7
    return has_only_digits_spaces_dash and is_long_enough

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def is_valid_full_name(full_name):
    return len(full_name) >= 1

def is_valid_user_name(user):
    # kept separated in case of validation rules change
    return is_valid_full_name(user)

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
