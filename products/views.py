import statistics, math

from django.http  import JsonResponse
from django.views import View

from .models      import Product, SubCategory, MainCategory, Image
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
            reviews          = Review.objects.filter(product_id = product_id)
            rating_list      = [review.rating for review in reviews]
            review_list      = [review.comment for review in reviews]

            for product in products:
                product_detail_data = {
                    "id"                 : product.id,
                    "name"               : product.name,
                    "price"              : format(round(product.price),","),
                    "description"        : product.description,
                    "images"             : [image.image_url for image in images],
                    "main_category_name" : MainCategory.objects.get(id = main_category_id).name,
                    "sub_category_name"  : SubCategory.objects.get(id = sub_category_id).name,
                    "store"              : get_product_information(product_id)[0],
                    "color"              : get_product_information(product_id)[1],
                    "size"               : get_product_information(product_id)[2],
                    "rating_average"     : math.floor(statistics.mean(rating_list) if len(rating_list) else 0),
                    "review_count"       : len(review_list),
                    "review_list"        : get_review_information(product_id),
                }

            return JsonResponse({"data" : product_detail_data}, status = 200)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "DOESNOTEXIST_PRODUCT_ID"}, status = 404)