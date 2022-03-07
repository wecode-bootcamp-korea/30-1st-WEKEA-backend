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
    
    for review in review_list:
        rating = review.rating
        sum += rating
        number_of_review += 1
    
    if number_of_review==0:
        return None

    average_rating=sum/number_of_review
    return average_rating

#product의 모든 정보와 defualt_filter_option을 리턴하는 함수
def get_product_data(sub_category_id):
    product_data_list   = []
    product_image_list = []   
    temp_defualt_store_option = {}
    temp_defualt_color_option = {}
    temp_defualt_size_option = {}  
    temp_defualt_max_price = 0   
    product_list=Product.objects.filter(sub_category_id=sub_category_id)
    
    for product_object in product_list:    
                product_image_list = [] 
                temp_store = {}
                temp_color = {}
                temp_size  = {}
                temp_remaining_stock = 0

                temp_defualt_max_price = max(temp_defualt_max_price,product_object.price)

                for image_object in product_object.image_set.all():
                    product_image_list.append(image_object.image_url)
                
                for productinformations in product_object.productinformation_set.all():
                    if productinformations.remaining_stock:
                        temp_store[productinformations.store.name] = True
                        temp_color[productinformations.color.name] = True
                        temp_size[productinformations.size.size]   = True
                        temp_remaining_stock = temp_remaining_stock + productinformations.remaining_stock
                        
                        #defualt option도 구해줌
                        temp_defualt_store_option[productinformations.store.name] = True
                        temp_defualt_color_option[productinformations.color.name] = True
                        temp_defualt_size_option[productinformations.size.size]   = True
                        
                
                product_data = {
                        'name'           : product_object.name,
                        'price'          : int(product_object.price),
                        'description'    : product_object.description,
                        #'average_rating' : carculate_average_rating(product_id),
                        'image_list'     : product_image_list,
                        'store_list'     : list(temp_store),
                        'color_list'     : list(temp_color),
                        'size_list'      : list(temp_size),
                        'remaining_stock' : temp_remaining_stock
                        }           
                product_data_list.append(product_data)
    
    default_filtering_options= {
        'price': int(temp_defualt_max_price), 
        'store': list(temp_defualt_store_option),
        'color': list(temp_defualt_color_option),
        'size' : list(temp_defualt_size_option)
        }

    return product_data_list , default_filtering_options     


#아직 미구현 함수
def get_filterd_product_id(filter_options):
    option_key_dict={'size':1,'color':2,'store':3,'min_price':4,'max_price':5,'discount':6,'sort':7}
    q=Q()
    target_product_id_list=[]
    options=filter_options.split(',')
    for option in options:
        option=str(option)
        key=option.split(':')[0]
        value_list=str(option.split(':')[1]).split('|')
        if value_list[0]!='null':  #만약 value가 null이 아닌 경우
            if option_key_dict[key]==1:
                for value in value_list:
                    q.add(Q(size=value) , q.OR)
                    print(q)
            elif option_key_dict[key]==2:
                print()
            elif option_key_dict[key]==3:
                print()  
            elif option_key_dict[key]==4:
                print()      
            elif option_key_dict[key]==5:
                print()
            elif option_key_dict[key]==6:
                print()
            elif option_key_dict[key]==7:
                print()    

class ProductListView(View):
    def get(self,request):
        try:
            result={}
            sub_category_id       = request.GET.get('sub_category_id')
            default_filter_bolean = request.GET.get('filter_bolean') #만약 값이 True이면 프론트에서 필터링을 적용한 데이터를 요구한것 False면 필터링 적용 안하고 가능한 옵션 
            filter_options        = request.GET.get('filter_option')
            
            #필터 예시
            filter_options ='size:X|XL|S,color:blue|black,store:광명점|기흥점,min_price:0,max_price:1000000,discount:null,sort:high-price'
                    
            if default_filter_bolean:  #필터링 적용 안하는 경우 
                    
                #1)subcategory를 외래키로 갖는 모든 product들을 저장
                product_data_list,default_filtering_options =get_product_data(sub_category_id)
                result['product_data_list']=product_data_list
                result['defualt_filter_options'] = default_filtering_options
                
                #2)제품의 카테고리를 출력 ex)의자/사무용의자
                SubCategory_object = SubCategory.objects.get(id=sub_category_id)
                sub_category_name  = SubCategory_object.name
                main_category_name = SubCategory_object.main_category.name
                product_hierarchy  = main_category_name+"/"+sub_category_name
                result['product_hierarchy']=product_hierarchy

            else: #필터링 적용했을 떄  (아직 미구현)
                get_filterd_product_id(filter_options)

            return JsonResponse({'message' : 'SUCCESS','result':result}, status = 201)

        except KeyError:
            return JsonResponse({"message": "KEY ERROR"}, status= 400)

