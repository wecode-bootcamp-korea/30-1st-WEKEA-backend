import re

from django.http import HttpResponse

from users.models import User, Cart, OrderProduct

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


def move_order_product(request, cart_id):
    user = request.user
    
    if cart_id == 0 :
        carts = Cart.objects.filter(user_id = user.id)

        for cart in carts:
            cart.product_information.remaining_stock -= cart.quantity
            cart.product_information.save()
            OrderProduct.objects.create(
                quantity = cart.quantity,
                order_status_id = 1, 
                product_information_id = cart.product_information.id, 
                user_id = user.id
            )
        carts.delete()
        return True

