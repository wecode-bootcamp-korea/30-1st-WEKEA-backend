import math

from django.http  import JsonResponse
from django.views import View
from django.db.models import Avg

from .models      import Discount, Product, ProductInformation, SubCategory, MainCategory, Image
from users.models import Review
from .utils       import get_product_information, get_review_information

class ProductDetailView(View):
    def get(self, request):
        try:
            product_id       = request.GET.get("product", None)
            products         = Product.objects.filter(id = product_id)
            images           = Image.objects.filter(product_id = product_id)
            sub_category_id  = Product.objects.get(id = product_id).sub_category_id
            main_category_id = SubCategory.objects.get(id = sub_category_id).main_category_id

            for product in products:
                product_detail_data = {
                    "id"                 : product.id,
                    "name"               : product.name,
                    "price"              : format(round(product.price),","),
                    "discount_price"     : format(math.floor(round(float(product.price) - \
                                        (float(product.price) * (product.discount.rate / 100)))),","),
                    "discount_rate"      : f"{product.discount.rate}%" ,
                    "description"        : product.description,
                    "images"             : [image.image_url for image in images],
                    "main_category_name" : MainCategory.objects.get(id = main_category_id).name,
                    "sub_category_name"  : SubCategory.objects.get(id = sub_category_id).name,
                    "store"              : get_product_information(product_id)[0],
                    "color"              : get_product_information(product_id)[1],
                    "size"               : get_product_information(product_id)[2],
                    "rating_average"     : math.floor(product.review_set.all().aggregate(Avg('rating'))['rating__avg']\
                                         if len(get_review_information(product_id)) != 0 else 0),
                    "review_count"       : product.review_set.count(),
                    "review_list"        : get_review_information(product_id),
                    "remaining_stock"    : get_product_information(product_id)[3],
                }

            return JsonResponse({"data" : product_detail_data}, status = 200)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "DOESNOTEXIST_PRODUCT_ID"}, status = 404)
