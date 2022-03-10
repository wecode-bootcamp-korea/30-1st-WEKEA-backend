from django.views               import View
from django.http                import JsonResponse
from .models                    import SubCategory,Product
from .utils                     import get_default_filtering_options, get_product_data,get_review_information, get_rating_average, get_discount_price, get_remaining_stock, get_option


class ProductListView(View):
    def get(self,request):
        try:       
            sub_category_id = request.GET.get('sub_category_id')    
            limit           = int(request.GET.get('limit',10))
            offset          = int(request.GET.get('offset',0))
            sort_option     = request.GET.get("sort",'default')
            filter_boolean  = request.GET.get("filter_boolean",False) 
            query_prams     = dict(request.GET)
            result           = {} 

            result['product_data_list'] = get_product_data(sort_option,limit,offset,query_prams)

            if filter_boolean == 'True': 
                result['default_filtering_options'] = get_default_filtering_options(sub_category_id)
            
            SubCategory_object            = SubCategory.objects.get(id=sub_category_id)
            product_hierarchy             = SubCategory_object.main_category.name+"/"+SubCategory_object.name
            result['product_hierarchy']   = product_hierarchy 
            result['product_description'] = SubCategory_object.description
           
            return JsonResponse({'result':result}, status = 200)

        except KeyError:
            return JsonResponse({"message": "KEY ERROR"}, status= 400)


class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product              = Product.objects.get(id = product_id)
            images               = product.image_set.all()

            product_detail_data = {
                "id"                 : product.id,
                "name"               : product.name,
                "price"              : product.price,
                "discount_price"     : get_discount_price(product_id),
                "discount_rate"      : product.discount.rate,
                "description"        : product.description,
                "images"             : [image.image_url for image in images],
                "main_category_name" : product.sub_category.main_category.name,
                "sub_category_name"  : product.sub_category.name,
                "store"              : get_option(product_id)["store"],
                "color"              : get_option(product_id)["color"],
                "size"               : get_option(product_id)["size"],
                "remaining_stock"    : get_remaining_stock(product_id),
                "rating_average"     : get_rating_average(product_id),
                "review_count"       : product.review_set.count(),
                "review_list"        : get_review_information(product_id),
            }

            return JsonResponse({"data" : product_detail_data}, status = 200)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "DOESNOTEXIST_PRODUCT_ID"}, status = 404)