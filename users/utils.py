import re

from users.models import User

def is_valid(data):
    email    = data["email"]
    password = data["password"]

    validation_email    = re.match(r"^(\w+[+-_.]?\w?)+@([\w+-_.]+[.][\w+-_.]+)$", email)
    validation_password = re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&?*])([a-zA-Z0-9!@#$%^&?*]){8,}$", password)

    if "" in data.values():
        return "EMPTY_DATA"

    if not validation_email:
        return "INVALID_EMAIL"

    if not validation_password:
        return "INVALID_PASSWORD"

    if User.objects.filter(email = email).exists():
        return "ALREADY_EXIST_EMAIL"

    return False


