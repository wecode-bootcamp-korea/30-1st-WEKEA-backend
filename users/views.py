import json

from django.http  import JsonResponse
from django.views import View

from .models         import User, Gender, OrderStatus, OrderProduct, Cart, Review
from products.models import Product, Image, SubCategory, MainCategory, ProductInformation, Store, Color, Size
from .validation     import email_validation, password_validation 


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            full_name    = data["full_name"]
            email        = data["email"]
            password     = data["password"]
            membership   = data["membership"]
            address      = data["address"]
            phone_number = data["phone_number"]
            gender_id    = data["gender_id"]

            if not email_validation(email):
                return JsonResponse({"MESSAGE" : "INVALID_EMAIL"})
            elif not password_validation(password):
                return JsonResponse({"MESSAGE" : "INVALID_PASSWORD"})

            if User.objects.filter(email = email).exists():
                return JsonResponse({"MESSAGE" : "ALREADY_EXIST_EMAIL"})
            
            User.objects.create(
                full_name    = full_name,
                eamil        = email,
                password     = password,
                membership   = membership,
                address      = address,
                phone_number = phone_number,
                gender_id    = gender_id
            )
            
            return JsonResponse({ "MESSAGE" : "SUCCESS"}, status = 200)

        except KeyError:
            return JsonResponse({ "MESSAGE" : "KEYERROR"}, status = 400)