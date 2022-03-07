from django.shortcuts import render

# Create your views here.

import json

from django.views           import View
from django.http            import JsonResponse
from django.db.utils        import IntegrityError
from django.core.exceptions import MultipleObjectsReturned
from django.db.models       import Q,Avg,Max,Sum
from .models                import Product,Image,SubCategory,MainCategory,ProductInformation,Store,Color,Size
from users.models           import Review
from math                   import floor

def get_product_data(sub_category_id,default_filter_bolean,q):
    product_data_list   = []
    product_image_list = []   
    temp_defualt_store_option = {}
    temp_defualt_color_option = {}
    temp_defualt_size_option = {}  
    
    if default_filter_bolean=="True":
        product_list=Product.objects.filter(sub_category_id=sub_category_id)
    else:
        product_list=Product.objects.filter(q)

    for product_object in product_list:    
                product_image_list = [] 
                temp_store = {}
                temp_color = {}
                temp_size  = {}

                average_rating    = product_object.review_set.all().aggregate(Avg('rating'))['rating__avg']
                product_image_list= [image_object.image_url for image_object in product_object.image_set.all()  ]

                

                for productinformations in product_object.productinformation_set.all(): #filter remaingstock 해주기
                    if productinformations.remaining_stock:
                        if not temp_store.get(productinformations.store.name) :
                            temp_store[productinformations.store.name] = True 
                        if not  temp_color.get(productinformations.color.name) :  
                            temp_color[productinformations.color.name] = True
                        if not temp_size.get(productinformations.size.size):
                            temp_size[productinformations.size.size]   = True
                        
                        if not temp_defualt_store_option.get(productinformations.store.name) :
                            temp_defualt_store_option[productinformations.store.name] = True 
                        if not  temp_defualt_color_option.get(productinformations.color.name) :  
                            temp_defualt_color_option[productinformations.color.name] = True
                        if not temp_defualt_size_option.get(productinformations.size.size):
                            temp_defualt_size_option[productinformations.size.size]   = True
                        
                        
                
                remaining_stock=product_object.productinformation_set.all().aggregate(Sum('remaining_stock'))['remaining_stock__sum']
                
                product_data = {
                        'name'           : product_object.name,
                        'price'          : int(product_object.price),
                        'description'    : product_object.description,
                        'average_rating' : floor(average_rating),
                        'image_list'     : product_image_list,
                        'store_list'     : list(temp_store),
                        'color_list'     : list(temp_color),
                        'size_list'      : list(temp_size),
                        'remaining_stock' : remaining_stock
                        }           
                product_data_list.append(product_data) #이 코드는 리스트 컴프리헨션을 쓰기 어렵다고 판단했습니다. 혹시 가능하다고 피드백 주시면 수정하겠습니다.

    defualt_max_price=product_list.aggregate(Max('price'))['price__max']
    default_filtering_options= {
        'max_price': int(defualt_max_price), 
        'store': list(temp_defualt_store_option),
        'color': list(temp_defualt_color_option),
        'size' : list(temp_defualt_size_option)
        }
        
    result={'product_data_list':product_data_list ,'default_filtering_options': default_filtering_options}
    
    return result    


def get_filterd_product_id(filter_options):
    q=Q()
    
    if filter_options['sub_category_id']:    
        q &=Q(sub_category_id=filter_options['sub_category_id'] )
    if filter_options['store']:
        q &=Q(productinformation__store__name__in=filter_options['store']) 
    if filter_options['color']:    
        q &=Q(productinformation__color__name__in=filter_options['color'])
    if filter_options['size']:    
        q &=Q(productinformation__size__size__in=filter_options['size'])
    if filter_options['min_price']:    
        q &=Q(price__gt=filter_options['min_price'] )
    if filter_options['max_price']:    
        q &=Q(price__lt=filter_options['max_price'] )

    return q
            
#orderby는 sort
class ProductListView(View):
    def get(self,request):
        # try:
            result                = {}
            sub_category_id       = request.GET.get('sub_category_id')
            default_filter_bolean = request.GET.get('filter_bolean') #만약 값이 "True이면 프론트에서 옵션 적용을 요구하지 않ㅇ느 것
            
            #offset range? 넣기
            print(default_filter_bolean)
            

            if default_filter_bolean=="True":  #필터링 적용 안하는 경우 
                    
                product_data = get_product_data(sub_category_id,default_filter_bolean,q=Q())
                result['product_data_list']=product_data['product_data_list']
                result['default_filtering_options'] = product_data['default_filtering_options']
                
                
                SubCategory_object = SubCategory.objects.get(id=sub_category_id)
                sub_category_name  = SubCategory_object.name
                main_category_name = SubCategory_object.main_category.name
                product_hierarchy  = main_category_name+"/"+sub_category_name
                result['product_hierarchy']=product_hierarchy

            else: 
                filter_options={
                    "sub_category_id" : request.GET.get('sub_category_id'),
                    "store"           : request.GET.getlist("store",None),
                    "color"           : request.GET.getlist("color",None),
                    "size"            : request.GET.getlist("size",None),
                    "min_price"       : request.GET.get("min_price",None),
                    "max_price"       : request.GET.get("max_price",None),
                    "discount"        : request.GET.get("discount",None)
                }
                
                q=get_filterd_product_id(filter_options)
                print()
                print()
                print("Q 객체는")
                print(q)
                print()
                print("필터값은")
                print(Product.objects.filter(q))

                product_data = get_product_data(sub_category_id,default_filter_bolean,q)
                result['product_data_list']=product_data['product_data_list']
                result['current_filtering_options'] = product_data['default_filtering_options']
                
                sort = request.GET.get("sort",None)
                
                

            return JsonResponse({'message' : 'SUCCESS','result':result}, status = 201)

        # except KeyError:
        #     return JsonResponse({"message": "KEY ERROR"}, status= 400)


