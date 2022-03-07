from django.shortcuts import render

# Create your views here.

import json

from django.views           import View
from django.http            import JsonResponse
from django.db.utils        import IntegrityError
from django.core.exceptions import MultipleObjectsReturned
from django.db.models       import Q 
from .models                import Product,Image,SubCategory,MainCategory,ProductInformation,Store,Color,Size
from users.models           import Review

#개별 product의 평균 rating을 구하는 메소드
def carculate_average_rating(product_id):
    average_rating   = 0
    sum              = 0
    number_of_review = 0
    review_list      = Review.objects.filter(product_id=product_id)
    
    for review in review_list.values():
        rating = review['rating']
        sum += rating
        number_of_review += 1
    
    if number_of_review==0:
        return None

    average_rating=sum/number_of_review
    return average_rating

#개별 product의 image_url을 리스트로 반환하는 메소드
def get_image_url_list(product_id):
    image_list        = []
    image_object_list = Image.objects.values().filter(product_id=product_id)
    for image_object in image_object_list:
        image_url = image_object['image_url']
        image_list.append(image_url)
 
    return image_list
#개별 product의 remaining_stock가 존재하는 store,color,size를 반환하는 메소드
def get_product_information(product_id):
    temp_store = {}
    temp_color = {}
    temp_size  = {}
    
    product_object_list=ProductInformation.objects.values().filter(product_id=product_id)

    for product_object in product_object_list:
        if product_object['remaining_stock']: #재고가 0이 아닐 경우
            product_store= Store.objects.values().get(id=product_object['store_id'])['name']
            product_color= Color.objects.values().get(id=product_object['color_id'])['name']
            product_size= Size.objects.values().get(id=product_object['size_id'])['size']
            
            temp_store[product_store] = True
            temp_color[product_color] = True
            temp_size[product_size]   = True
            

    return list(temp_store), list(temp_color), list(temp_size)


#product의 모든 정보를 리턴하는 함수
def get_product_data(product_id_list):
    product_data_list   = []          
    
    for product_id in product_id_list:    
                store_list, color_list, size_list = get_product_information(product_id)
                product_object=Product.objects.values().get(id=product_id)
                product_data = {
                    'name'           : product_object['name'],
                    'price'          : int(product_object['price']),
                    'description'    : product_object["description"],
                    'average_rating' : carculate_average_rating(product_id),
                    'image_list'     : get_image_url_list(product_id),
                    'store_list'     : store_list,
                    'color_list'     : color_list,
                    'size_list'      : size_list
                    }        
                product_data_list.append(product_data)
    
    return product_data_list     
        
#해당 subcategory의 모든 옵션들을 리턴하는 함수
def get_defualt_filter_options(product_data_list):
    temp_default_filtering_option = {"price":{} ,"store":{}, "color":{}, "size":{} } 
    for product_data in product_data_list:

            temp_default_filtering_option["price"][product_data["price"]]=True
            for store in product_data['store_list']:
                temp_default_filtering_option["store"][store]=True
            for color in product_data['color_list']:
                temp_default_filtering_option["color"][color]=True
            for size in product_data['size_list']:
                temp_default_filtering_option["size"][size]=True    
    
    default_filter_price=list(temp_default_filtering_option['price'])
    default_filter_store=list(temp_default_filtering_option['store'])
    default_filter_color=list(temp_default_filtering_option['color'])
    default_filter_size=list(temp_default_filtering_option['color'])
    default_filter_price.sort(reverse=True)
    print
    default_filtering_option= {
        'price': default_filter_price, 
        'store': default_filter_store,
        'color': default_filter_color,
        'size' : default_filter_size
        }

    return default_filtering_option
#아직 미구현 함수
def get_filterd_product_id(filter_options):
    option_key_dict={'size':1,'color':2,'store':3,'discount':4,'sort':5}
    q=Q()
    target_product_id_list=[]
    options=filter_options.split(',')
    for option in options:
        option=str(option)
        key=option.split(':')[0]
        value_list=str(option.split(':')[1]).split('|')
        if value_list[0]!='null':  #만약 value가 null이 아닌 경우
            print("미구현")


class ProductListView(View):
    def get(self,request):
        try:
            result={}
            sub_category_id       = request.GET.get('sub_category_id')
            default_filter_bolean = request.GET.get('filter_bolean') #만약 값이 True이면 프론트에서 필터링을 적용한 데이터를 요구한것 False면 필터링 적용 안하고 가능한 옵션 
            filter_options        = request.GET.get('filter_option')
            
            #필터 예시
            filter_options ='size:X|XL|S,color:blue|black,store:광명점|기흥점,discount:null,sort:high-price'
                    
            if default_filter_bolean:  #필터링 적용했을 떄  (아직 미구현)
                 get_filterd_product_id(filter_options)

            else: #필터링 적용 안함 
                product_list     = Product.objects.values().filter(sub_category_id=sub_category_id) 
                product_id_list  = []
                for product_object in product_list: #product_id만 리스트에 저장
                        product_id_list.append(product_object["id"])
                #1)subcategory를 외래키로 갖는 모든 product들을 저장
                product_data_list=get_product_data(product_id_list)
                result['product_data_list']=product_data_list

                #2)가능한 모든 경우의 옵션을 저장 (소비자가 처음 보는 화면의 필터링 옵션ㄹ퓨 )
                defualt_filter_options           = get_defualt_filter_options(product_data_list)
                result['defualt_filter_options'] = defualt_filter_options
            
            return JsonResponse({'message' : 'SUCCESS','result':result}, status = 201)

        except KeyError:
            return JsonResponse({"message": "KEY ERROR"}, status= 400)

