import math

from django.db.models import Avg, Sum

from .models      import Product
from users.models import Review

def get_option(product_id):
    product              = Product.objects.get(id = product_id)
    product_informations = product.productinformation_set.all()

    store = [product_information.store.name for product_information in product_informations]
    color = [product_information.color.name for product_information in product_informations]
    size  = [product_information.size.size for product_information in product_informations]

    return {"store" : list(set(store)), "color" : list(set(color)), "size" : list(set(size))}


def get_review_information(product_id):
    product     = Product.objects.get(id = product_id)
    reviews     = product.review_set.all()
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


def get_rating_average(product_id):
    product = Product.objects.get(id = product_id)
    reviews = product.review_set.all()

    rating_average = math.floor(reviews.aggregate(Avg('rating'))['rating__avg']\
                    if product.review_set.count() != 0 else 0)

    return rating_average


def get_discount_price(product_id):
    product = Product.objects.get(id = product_id)

    discount_price = product.price - (product.price * product.discount.rate / 100)

    return discount_price


def get_remaining_stock(product_id):
    product              = Product.objects.get(id = product_id)
    product_informations = product.productinformation_set.all()

    remaining_stock = product_informations.aggregate(Sum("remaining_stock"))["remaining_stock__sum"]

    return remaining_stock