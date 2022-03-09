import json
from operator                   import itemgetter
from django.views               import View
from django.http                import JsonResponse
from django.db.utils            import IntegrityError
from django.core.exceptions     import MultipleObjectsReturned
from django.db.models           import Q,Avg,Max,Sum,F,Subquery
from django.shortcuts           import render
from django.db.models.functions import Coalesce
from .models                    import Product,Image,SubCategory,MainCategory,ProductInformation,Store,Color,Size
from users.models               import Review
from math                       import floor

def get_defualt_filtering_options (sub_category_id):
    defualt_store_options = []
    defualt_color_options = []
    defualt_size_options  = []
    
    product_list = Product.objects.filter(sub_category_id=sub_category_id)
    
    defualt_max_price = product_list.aggregate(Max('price'))['price__max']
    if not defualt_max_price:
        defualt_max_price=0
        
    for product_object in product_list:
        productinformations=product_object.productinformation_set.all()
        
        temp_product_store_list = [productinformation.store.name for productinformation in productinformations]
        temp_product_color_list = [productinformation.color.name for productinformation in productinformations]
        temp_product_size_list  = [productinformation.size.size for productinformation in productinformations]
        
        defualt_store_options.extend(temp_product_store_list)
        defualt_color_options.extend(temp_product_color_list)
        defualt_size_options.extend(temp_product_size_list)
    
    default_filtering_options= {
        'max_price': int(defualt_max_price), 
        'store': list(set(defualt_store_options)),
        'color': list(set(defualt_color_options)),
        'size' : list(set(defualt_size_options))
        }

    return default_filtering_options


def get_product_data(sort_option,q,limit,offset):
    product_data_list  = []
    product_image_list = []   
     
    product_list = Product.objects.filter(q).distinct().annotate(average_rating=Avg('review__rating'))
    
    sort_option_dict = {'high-price':'-price', 'low-price':'price' ,'created':'-created_at','rating':'-average_rating'}   
    if sort_option_dict.get(sort_option,''):
        product_list     = product_list.order_by(sort_option_dict[sort_option])
    
    for product_object in product_list[offset:offset+limit]:    
                product_image_list = [] 
                
                average_rating=product_object.average_rating
                if not average_rating:
                    average_rating=0

                productinformations = product_object.productinformation_set.filter(remaining_stock__gt=0)
                product_store_list  = list(set([productinformation.store.name for productinformation in productinformations]))
                product_color_list  = list(set([productinformation.color.name for productinformation in productinformations]))
                product_size_list   = list(set([productinformation.size.size for productinformation in productinformations]))
                
                product_image_list  = [image_object.image_url for image_object in product_object.image_set.all()]
                         
                remaining_stock     = product_object.productinformation_set.all().aggregate(Sum('remaining_stock'))['remaining_stock__sum']  
                product_data = {
                        'name'             : product_object.name,
                        'price'            : int(product_object.price),
                        'description'      : product_object.description,
                        'average_rating'   : floor(average_rating),
                        'image_list'       : product_image_list,
                        'store_list'       : product_store_list,
                        'color_list'       : product_color_list,
                        'size_list'        : product_size_list,
                        'remaining_stock'  : remaining_stock,
                        'discount'         : product_object.discount.rate,
                        'discounted_price' : int(product_object.price) -  int(int(product_object.price) * product_object.discount.rate / 100)
                        }           
                
                product_data_list.append(product_data) 
    
    return product_data_list   

def get_Q(filter_options):
    q=Q(sub_category_id=filter_options['sub_category_id'])   

    if filter_options['store']:
        q &=Q(productinformation__store__name__in = filter_options['store']) 
    if filter_options['color']: 
        q &=Q(productinformation__color__name__in = filter_options['color'])
    if filter_options['size']:    
        q &=Q(productinformation__size__size__in = filter_options['size'])
    if filter_options['min_price']:  
        q &=Q(price__gte = filter_options['min_price'] )
    if filter_options['max_price']:    
        q &=Q(price__lte = filter_options['max_price'] )
    if filter_options['discount']:    
        discount_list = [int(discount_rate) for discount_rate in filter_options['discount'] ]
        q &=Q(discount__rate__in = discount_list)
    
    return q
            

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
            
            SubCategory_object          = SubCategory.objects.get(id=filter_options['sub_category_id'])
            product_hierarchy           = SubCategory_object.main_category.name+"/"+SubCategory_object.name
            result['product_hierarchy'] = product_hierarchy
            
            return JsonResponse({'message' : 'SUCCESS','result':result}, status = 201)

        except KeyError:
            return JsonResponse({"message": "KEY ERROR"}, status= 400)


