import json, bcrypt, jwt

from datetime               import datetime, timedelta
from django.http            import HttpResponse, JsonResponse
from django.views           import View
from django.db.models       import F
from django.core.exceptions import MultipleObjectsReturned

from .models                import User, Cart, OrderProduct
from .utils                 import is_valid, move_order_product
from .decorator             import login_decorator
from products.models        import ProductInformation
from products.utils         import get_discount_price
from my_settings            import SECRET_KEY, ALGORITHM    


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            validation_result = is_valid(data)
            
            if not validation_result:
                return JsonResponse({"message" : "INVALID_INPUT_INFORMATION"}, status = 400)
            
            full_name         = data["full_name"]
            email             = data["email"]
            membership        = data["membership"]
            address           = data["address"]
            phone_number      = data["phone_number"]
            gender_id         = data["gender_id"]
            password          = data["password"]
            hashed_password   = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

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
            payload      = {'user' : user.id, 'exp' : datetime.now() + timedelta(hours=1)}
            access_token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400)
                            
            return JsonResponse({"access_token" : access_token}, status = 200)

        except KeyError:
            return JsonResponse({"message" : "KEYERROR"}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status = 400)


class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            user        = request.user
            cart_id     = data["cart_id"]

            if move_order_product(request, cart_id):
                return HttpResponse(status = 201)

            color_id    = data["color_id"]
            product_id  = data["product_id"]
            size_id     = data["size_id"]

            productinformation = ProductInformation.objects.get(color_id = color_id, size_id = size_id, product_id = product_id)
            remaining_stock    = ProductInformation.objects.get(id = productinformation.id).remaining_stock

            if not ProductInformation.objects.filter(id = productinformation.id).exists():
                return JsonResponse({"message" : "INVALID_OPTION"}, status = 404)
            
            if remaining_stock <= 0:
                return JsonResponse({"message" : "LACK_OF_QUANTITY"}, status = 400)


            cart, created = Cart.objects.get_or_create(
                user_id                = user.id,
                product_information_id = productinformation.id,
                defaults               = {"quantity" : 1}
            )
            
            if not created:
                if cart.quantity >= remaining_stock:
                    return JsonResponse({"message" : "LACK_OF_QUANTITY"}, status = 400)
                else:
                    cart.quantity = F("quantity") + 1

            cart.save()
            
            return HttpResponse(status = 201)

        except KeyError: 
            return JsonResponse({"message" : "KEYERROR" }, status = 400)

        except ProductInformation.DoesNotExist:
            return JsonResponse({"message" : "INVALID_PRODUCT_INFORMATION"}, status = 400)

    @login_decorator
    def get(self, request):
        user  = request.user
        
        if not Cart.objects.filter(user_id = user.id).exists():
            return JsonResponse({"message" : "USER_NOT_EXISTS" }, status = 400)
        
        carts   = Cart.objects.filter(user_id = user.id)
        results = [
            {
                "cart_id"       : cart.id,
                "quantity"      : cart.quantity,
                "stock"         : cart.product_information.remaining_stock,
                "image"         : cart.product_information.product.image_set.all()[0].image_url if len(cart.product_information.product.image_set.all()) != 0 else None,
                "main_category" : cart.product_information.product.sub_category.main_category.name,
                "sub_category"  : cart.product_information.product.sub_category.name,
                "product_name"  : cart.product_information.product.name,
                "product_id"    : cart.product_information.product.id,
                "color"         : cart.product_information.color.name,
                "size"          : cart.product_information.size.size,
                "price"         : cart.product_information.product.price,
                "discount"      : get_discount_price(cart.product_information.product.id)
            } for cart in carts
        ]
        
        return JsonResponse({"result" : results}, status = 200)

    @login_decorator
    def patch(self, request):
        try:
            data = json.loads(request.body)

            user     = request.user
            cart_id  = data["cart_id"]
            quantity = data["quantity"]
          
            cart          = Cart.objects.get(user_id = user.id, id = cart_id)
            cart.quantity = quantity
            
            if cart.quantity > cart.product_information.remaining_stock:
                return JsonResponse({"message" : "LACK_OF_QUANTITY"}, status = 400)

            cart.save()

            if cart.quantity == 0:
                cart.delete()

            return JsonResponse({"message" : "SUCCESS"}, status = 200)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        except Cart.DoesNotExist:
            return JsonResponse({"message" : "CART_DOES_NOT_EXIST"}, status = 400)
            
    @login_decorator
    def delete(self,request):
        try:
            data    = json.loads(request.body)

            user    = request.user
            cart_id = data["cart_id"]

            cart = Cart.objects.get(user_id = user.id , id= cart_id)

            if cart:
                cart.delete()

            return HttpResponse(status = 204)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        except Cart.DoesNotExist:
            return JsonResponse({"message" : "CART_DOES_NOT_EXIST"}, status = 400)

        except MultipleObjectsReturned:
            Cart.objects.filter(user_id = user.id, id= cart_id).first()
