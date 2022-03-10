import re, bcrypt

from users.models import User

def is_valid(data):
    email    = data["email"]
    password = data["password"]

    validation_email    = re.match(r"^(\w+[+-_.]?\w?)+@([\w+-_.]+[.][\w+-_.]+)$", email)
    validation_password = re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&?*])([a-zA-Z0-9!@#$%^&?*]){8,}$", password)

    if User.objects.filter(email = email).exists():
        return False

    if not validation_email:
        return False

    if not validation_password:
        return False

    return True


