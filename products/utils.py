from django.db.models import Q

from .models      import ProductInformation
from users.models import Review

def get_product_information(product_id):
    temp_store      = set()
    temp_color      = set()
    temp_size       = set()

    products = ProductInformation.objects.filter(Q(product_id = product_id) or Q(remaining_stock = 0))
    zero_stock = [{"store" : list(set(product.store.name)), "color" : list(set(product.color.name)), "size" : list(set(product.size.size))} \
                for product in products if product.remaining_stock == 0]

    for product in products:
        temp_store.add(product.store.name)
        temp_color.add(product.color.name)
        temp_size.add(product.size.size)


    store_list = list(temp_store)
    color_list = list(temp_color)
    size_list  = list(temp_size)
    store_list.sort()

    return store_list, color_list, size_list, zero_stock

def get_review_information(product_id):
    reviews     = Review.objects.filter(product_id = product_id)
    review_list = []

    for review in reviews:
        email = review.user.email
        review_information = {
            "user_name" : review.user.full_name,
            "user_email" : email.replace(email[3:email.index("@")],"*" * 4),
            "created_date" : review.created_at.strftime("%Y-%m-%d"),
            "rating" : review.rating,
            "commnet" : review.comment
        }
        review_list.append(review_information)

    return review_list