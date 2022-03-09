from django.views               import View
from django.http                import JsonResponse
from .models                    import SubCategory
from .utils                     import get_defualt_filtering_options, get_product_data, get_Q


class ProductListView(View):
    def get(self,request):
        try:       
            sub_category_id = request.GET.get('sub_category_id')    
            limit           = int(request.GET.get('limit',10))
            offset          = int(request.GET.get('offset',0))
            sort_option     = request.GET.get("sort",None)
            filter_boolean   = request.GET.get("filter_boolean",False) 

            filter_options={
                    'sub_category_id' : sub_category_id,
                    "store"           : request.GET.getlist("store",None),
                    "color"           : request.GET.getlist("color",None),
                    "size"            : request.GET.getlist("size",None),
                    "min_price"       : request.GET.get("min_price",None),
                    "max_price"       : request.GET.get("max_price",None),
                    "discount"        : request.GET.getlist("discount",None)
                }  
            q = get_Q(filter_options)

            result                              = {} 
            result['product_data_list']         = get_product_data(sort_option,q,limit,offset)

            if filter_boolean == 'False': #False 일 때 프론트에서 get_defualt_filtering_options을 요구하는 것으로 합의 됨
                result['default_filtering_options'] = get_defualt_filtering_options (sub_category_id)
            
            SubCategory_object            = SubCategory.objects.get(id=filter_options['sub_category_id'])
            product_hierarchy             = SubCategory_object.main_category.name+"/"+SubCategory_object.name
            result['product_hierarchy']   = product_hierarchy 
            result['product_description'] = SubCategory_object.description
            
            return JsonResponse({'message' : 'SUCCESS','result':result}, status = 201)

        except KeyError:
            return JsonResponse({"message": "KEY ERROR"}, status= 400)


