import json, bcrypt, jwt

from datetime     import datetime, timedelta
from django.http  import HttpResponse, JsonResponse
from django.views import View

from .models      import User
from .utils       import is_valid
from my_settings  import SECRET_KEY, ALGORITHM    


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            validation_result = is_valid(data)
            full_name         = data["full_name"]
            email             = data["email"]
            membership        = data["membership"]
            address           = data["address"]
            phone_number      = data["phone_number"]
            gender_id         = data["gender_id"]
            password          = data["password"]
            hashed_password   = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            if not validation_result:
                return JsonResponse({"message" : "INVALID_INPUT_INFORMATION"}, status = 400)

            User.objects.create(
                full_name    = full_name,
                email        = email,
                password     = hashed_password,
                membership   = membership,
                address      = address,
                phone_number = phone_number,
                gender_id    = gender_id
            )
            
            return HttpResponse(status = 201)

        except KeyError:
            return JsonResponse({"message" : "KEYERROR"}, status = 400)


class LogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email        = data["email"]
            password     = data["password"]
            user         = User.objects.get(email = email)
            payload      = {'user' : user.id, 'exp' : datetime.now() + timedelta(days=1)}
            access_token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400)
                            
            return JsonResponse({"access_token" : access_token}, status = 200)

        except KeyError:
            return JsonResponse({"message" : "KEYERROR"}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status = 400)
