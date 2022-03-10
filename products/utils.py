from django.db.models           import Q,Avg,Max,Sum
from .models                    import Product
from math                       import floor

def get_default_filtering_options(sub_category_id):
    defualt_store_options = []
    defualt_color_options = []
    defualt_size_options  = []
    
    product_list = Product.objects.filter(sub_category_id=sub_category_id)
    
    defualt_max_price = product_list.aggregate(Max('price'))['price__max'] if product_list.aggregate(Max('price'))['price__max'] else 0
    
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
        'store'    : list(set(defualt_store_options)),
        'color'    : list(set(defualt_color_options)),
        'size'     : list(set(defualt_size_options))
        }

    return default_filtering_options


def get_product_data(sort_option,limit,offset,query_prams):
    product_data_list  = []
    product_image_list = []   

    q  =Q(sub_category_id=query_prams['sub_category_id'][0])   
    
    if query_prams.get('discount',None):    
        discount_list = [int(discount_rate) for discount_rate in query_prams['discount'][0] ]
        q &=Q(discount__rate__in = discount_list)

    field_lookup_dict= {
        'store'     : 'productinformation__store__name__in',
        'size'      : 'productinformation__size__size__in',
        'color'     : 'productinformation__color__name__in',
        'min_price' : 'price__gte',
        'max_price' :'price__lte' 
        }
        
    filter_set = { field_lookup_dict.get(key) :value for key, value  in query_prams.items() }
    filter_set.pop(None)
    
    product_list = Product.objects.filter(q,**filter_set).distinct().annotate(average_rating=Avg('review__rating'))
    
    sort_option_dict = {
        'high-price' : '-price', 
        'low-price'  : 'price' ,
        'created'    : '-created_at',
        'rating'     : '-average_rating',
        'default'    : 'id'
        }   

    product_list = product_list.order_by(sort_option_dict[sort_option])
    
    for product_object in product_list[offset:offset+limit]:    
                average_rating     = product_object.average_rating if product_object.average_rating  else 0
                product_image_list  = [image_object.image_url for image_object in product_object.image_set.all()]
                productinformations = product_object.productinformation_set.filter(remaining_stock__gt=0)
                product_store_list  = list(set([productinformation.store.name for productinformation in productinformations]))
                product_color_list  = list(set([productinformation.color.name for productinformation in productinformations]))
                product_size_list   = list(set([productinformation.size.size for productinformation in productinformations]))          
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
                        'discounted_price' : int(product_object.price) - int(int(product_object.price) * product_object.discount.rate / 100)
                        }           
                
                product_data_list.append(product_data) 
    
    return product_data_list   


