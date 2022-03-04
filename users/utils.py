import re, jwt

from functools import wraps

from django.http import JsonResponse

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

def validation_email(email):
    EMAIL_REGEX = re.compile(r"^(\w+[+-_.]?\w?)+@([\w+-_.]+[.][\w+-_.]+)$")
    return re.match(EMAIL_REGEX, email)

def validation_password(password):
    PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&?*])([a-zA-Z0-9!@#$%^&?*]){8,}$")
    return re.match(PASSWORD_REGEX, password)

def login_decorator(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user_id      = User.objects.get(id = payload["id"])

            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({ "message" : "INVALID_TOKEN"}, status = 401)
        
        except User.DoesNotExist:
            return JsonResponse({ "message" : "INVALID_USER"}, status = 401)

    return wrapper