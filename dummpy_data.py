import os, django, csv, sys
from re import sub
from decimal import Decimal
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wekea.settings')
django.setup()

from users.models import *
from products.models import *

CSV_PATH_PRODUCT_DATA = './data_products.csv'
CSV_PATH_USER_DATA = './data_users.csv'

def insert_independent_table():
    with open(CSV_PATH_PRODUCT_DATA, 'rt',  encoding='UTF8') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        next(data_reader, None)

        for row in data_reader:
           
            # main_categories
                if row[1]:
                    name = row[1]
                    MainCategory.objects.create(name=name)
            
            # sub_categories    
                if row[3]:
                    name=row[3]
                    main_category_id=row[4]
                    description=row[5]
                    sub_image_url=row[6]
                    SubCategory.objects.create(name=name,main_category_id=main_category_id,description=description,image_url=sub_image_url)

              #discount
                if row[14]:
                    type=row[14]
                    rate=row[15]
                    Discount.objects.create(type=type,rate=rate)
                
            

            #stores
                if row[26]:
                    name=row[26]
                    Store.objects.create(name=name)

            #colors
                if row[28]:
                    name=row[28]
                    Color.objects.create(name=name)

            #sizes
                if row[30]:
                    size=row[30]
                    Size.objects.create(size=size)

def insert_product():
    #product
    with open(CSV_PATH_PRODUCT_DATA, 'rt',  encoding='UTF8') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        next(data_reader, None)    
        for row in data_reader:        
            if row[8]:
                name=row[8]
                price= row[9]
                price=float(price.replace(',',''))
                description=row[10]
                sub_category_id=int(row[11])
                discount_id=row[12]
                Product.objects.create(name=name,price=price,description=description,sub_category_id=sub_category_id,discount_id=discount_id)


def insert_image_information():            
    #images
    with open(CSV_PATH_PRODUCT_DATA, 'rt',  encoding='UTF8') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        next(data_reader, None)
        for row in data_reader:
            if row[17]:
                    image_url=row[17]
                    product_id=row[18] 
                    Image.objects.create(image_url=image_url,product_id=product_id)                        
                        
def insert_products_information():
    with open(CSV_PATH_PRODUCT_DATA, 'rt',  encoding='UTF8') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        next(data_reader, None)

        for row in data_reader:
           
             #ProductInformation
                if row[20]:
                    product_id=row[20]
                    store_id=row[21]
                    color_id=row[22]
                    size_id=row[23]
                    remaining_stock=row[24]
                    ProductInformation.objects.create(product_id=product_id,store_id=store_id,color_id=color_id,size_id=size_id,remaining_stock=remaining_stock)

                                
            

def insert_genders_order_status():
    with open(CSV_PATH_USER_DATA, 'rt',  encoding='UTF8') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        next(data_reader, None)
        
        for row in data_reader:
           
            #genders
            if row[9]:
                gender=row[9]
                Gender.objects.create(gender=gender)

            #order_status
            if row[20]:
                status=row[20]
                OrderStatus.objects.create(status=status)

def insert_users():
    with open(CSV_PATH_USER_DATA, 'rt',  encoding='UTF8') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        next(data_reader, None)
        
        for row in data_reader:
        
            #users
            if row[1]:
                full_name=row[1]
                email=row[2]
                password=row[3]
                membership=row[4]
                if membership=="TRUE":
                   membership=True
                else:
                   membership=False
                address=row[5]
                phone_number=row[6]
                gender_id=int(row[7])
                User.objects.create(full_name=full_name,email=email,password=password,membership=membership,address=address,phone_number=phone_number,gender_id=gender_id)

          
def insert_orderProducts_cart():
    with open(CSV_PATH_USER_DATA, 'rt',  encoding='UTF8') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        next(data_reader, None)
        
        for row in data_reader:
        
            #carts
            if row[11]:
                quantity=row[11]
                user_id=row[12]
                product_information_id=row[13]
                
                Cart.objects.create(quantity=quantity,user_id=user_id,product_information_id=product_information_id)
            
            #order_products
            if row[15]:
                quantity=row[15]
                order_status_id=row[16]
                user_id=row[17]
                product_information_id=row[18]

                OrderProduct.objects.create(quantity=quantity,order_status_id=order_status_id,user_id=user_id,product_information_id=product_information_id)
                
def insert_reviews():
    with open(CSV_PATH_USER_DATA, 'rt',  encoding='UTF8') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        next(data_reader, None)
        
        for row in data_reader:
        
            #carts
            if row[22]:
                rating=row[22]
                comment=row[23]
                user_id=int(row[24])
                product_id=int(row[25])
                
                Review.objects.create(rating=rating,comment=comment,user_id=user_id,product_id=product_id)

insert_independent_table()
insert_product()
insert_products_information()
insert_image_information()
insert_genders_order_status()
insert_users()


insert_orderProducts_cart()
insert_reviews()
print("더미데이터 삽입 완료")