import re

def email_validation(email):
    EMAIL_REGEX = re.match(r"^(\w+[+-_.]?\w?)+@([\w+-_.]+[.][\w+-_.]+)$", email)
    return EMAIL_REGEX

def password_validation(password):
    PASSWORD_REGEX = re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&?*])([a-zA-Z0-9!@#$%^&?*]){8,}$", password)
    return PASSWORD_REGEX