from django.shortcuts import render

# Create your views here.

import json

from django.views           import View
from django.http            import JsonResponse
from django.db.utils        import IntegrityError
from django.core.exceptions import MultipleObjectsReturned

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
    image_list=[]
    image_object_list=Image.objects.values().filter(product_id=product_id)
    for image_object in image_object_list:
        image_url=image_object['image_url']
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
            temp_store[Store.objects.values().get(id=product_object['store_id'])['name']] = True
            temp_color[Color.objects.values().get(id=product_object['color_id'])['name']] = True
            temp_size[Size.objects.values().get(id=product_object['size_id'])['size']]    = True
    
    store_list = list(temp_store)
    color_list = list(temp_color)
    size_list  = list(temp_size)
    
    return store_list, color_list, size_list

class ProductListView(View):
    def get(self,request):
        try:
            store_list      = color_list=size_list=[]
            sub_category_id = self.request.GET.get('sub_category_id')
            product_list    = Product.objects.values().filter(sub_category_id=sub_category_id)
            result          = []

            for product in product_list:    
                store_list, color_list, size_list = get_product_information(product['id'])
                product_data = {
                    'name':product['name'],
                    'price':int(product['price']),
                    'description':product["description"],
                    'average_rating' :carculate_average_rating(product['id']),
                    'image_list': get_image_url_list(product['id']),
                    'store_list':store_list,
                    'color_list':color_list,
                    'size_list':size_list
                    }
                result.append(product_data)
            
            return JsonResponse({'message' : 'SUCCESS','result':result}, status = 201)

        except KeyError:
            return JsonResponse({"message": "KEY ERROR"}, status= 400)

