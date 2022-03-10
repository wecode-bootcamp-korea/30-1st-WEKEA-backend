from django.views               import View
from django.http                import JsonResponse
from .models                    import SubCategory,Product,DefaultFilteringOption
from .utils                     import get_default_filtering_options, get_product_data,get_review_information, get_rating_average, get_discount_price, get_remaining_stock, get_option
import pickle
import ast

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

            byte_string                         = DefaultFilteringOption.objects.get(sub_category_id=sub_category_id).defualt_filtering_options
            result['default_filtering_options'] = pickle.loads(ast.literal_eval(byte_string))

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
            
            
class UpdateSubCategoryView(View):
    def patch(self, request):
           
            if DefaultFilteringOption.objects.exists(): #기존에 데이터가 있을 경우 UPDATE
                default_filtering_option_list=DefaultFilteringOption.objects.all()
                for default_filtering_option_obejct in default_filtering_option_list:
                    default_filtering_option_obejct.defualt_filtering_options = pickle.dumps(get_default_filtering_options(default_filtering_option_obejct.sub_category.id))
                    default_filtering_option_obejct.save()
            
            else: #만약 기존에 DefaultFilteringOption가 비어있을 경우
                sub_category_list=SubCategory.objects.all()
                for sub_category_obeject in sub_category_list:
                    sub_category_id           = sub_category_obeject.id
                    defualt_filtering_options = get_default_filtering_options(sub_category_obeject.id)
                    
                    DefaultFilteringOption.objects.create(sub_category_id = sub_category_id,defualt_filtering_options=defualt_filtering_options)
                
            return JsonResponse({"message" : "SUCCESS"}, status = 200)
       