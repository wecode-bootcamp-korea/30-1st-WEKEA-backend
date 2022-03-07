import jwt

from functools    import wraps

from django.http  import JsonResponse

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

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