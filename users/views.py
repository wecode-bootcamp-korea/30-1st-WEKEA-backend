import json, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View

from .models     import User
from .utils import email_validation, password_validation
from my_settings import SECRET_KEY, ALGORITHM    


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            full_name       = data["full_name"]
            email           = data["email"]
            membership      = data["membership"]
            address         = data["address"]
            phone_number    = data["phone_number"]
            gender_id       = data["gender_id"]
            password        = data["password"]
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            if not email_validation(email):
                return JsonResponse({"MESSAGE" : "INVALID_EMAIL"})
            elif not password_validation(password):
                return JsonResponse({"MESSAGE" : "INVALID_PASSWORD"})

            if User.objects.filter(email = email).exists():
                return JsonResponse({"MESSAGE" : "ALREADY_EXIST_EMAIL"})
            
            User.objects.create(
                full_name    = full_name,
                email        = email,
                password     = hashed_password,
                membership   = membership,
                address      = address,
                phone_number = phone_number,
                gender_id    = gender_id
            )
            
            return JsonResponse({ "MESSAGE" : "SUCCESS" }, status = 201)

        except KeyError:
            return JsonResponse({ "MESSAGE" : "KEYERROR" }, status = 400)


class LogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data["email"]
            password = data["password"]

            if not User.objects.filter(email = email).exists():
                return JsonResponse({ "MESSAGE" : "INVALID_USER" }, status = 400)

            user         = User.objects.get(email = email)
            access_token = jwt.encode({'id' : user.id}, SECRET_KEY, ALGORITHM)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({ "MESSAGE" : "INVALID_PASSWORD" }, status = 400)
                            
            return JsonResponse({ "MESSAGE" : "SUCCESS", "ACCESS_TOKEN" : access_token }, status = 201)

        except KeyError:
            return JsonResponse({ "MESSAGE" : "KEYERROR" }, status = 400)
