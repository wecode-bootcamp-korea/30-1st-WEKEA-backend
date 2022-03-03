import re, jwt

from functools import wraps

from django.http import JsonResponse

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

def email_validation(email):
    EMAIL_REGEX = re.match(r"^(\w+[+-_.]?\w?)+@([\w+-_.]+[.][\w+-_.]+)$", email)
    return EMAIL_REGEX

def password_validation(password):
    PASSWORD_REGEX = re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&?*])([a-zA-Z0-9!@#$%^&?*]){8,}$", password)
    return PASSWORD_REGEX

def login_decorator(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user         = User.objects.get(id = payload["id"])
            request.user = user

            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({ "MESSAGE" : "INVALID_TOKEN"}, status = 401)
        
        except User.DoesNotExist:
            return JsonResponse({ "MESSAGE" : "INVALID_USER"}, status = 401)

    return wrapper