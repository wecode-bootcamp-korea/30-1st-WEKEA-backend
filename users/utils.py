import re, jwt

from functools import wraps

from django.http import JsonResponse

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

def is_valid(data):
    validation_email    = re.match(r"^(\w+[+-_.]?\w?)+@([\w+-_.]+[.][\w+-_.]+)$", data["email"])
    validation_password = re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&?*])([a-zA-Z0-9!@#$%^&?*]){8,}$", data["password"])

    if "" in data.values():
        return "EMPTY_DATA"

    if not validation_email:
        return "INVALID_EMAIL"

    if not validation_password:
        return "INVALID_PASSWORD"

    if User.objects.filter(email = data["email"]).exists():
        return "ALREADY_EXIST_EMAIL"

    return False


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
            return JsonResponse({"message" : "INVALID_TOKEN"}, status = 401)
        
        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status = 401)

    return wrapper
    