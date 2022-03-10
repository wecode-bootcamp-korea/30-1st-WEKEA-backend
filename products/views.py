from django.views               import View
from django.http                import JsonResponse
from .models                    import SubCategory
from .utils                     import get_default_filtering_options, get_product_data


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


