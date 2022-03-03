import os, django, csv, sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wekea.settings')
django.setup()

from users.models import *
from products.models import *

CSV_PATH_PRODUCT_DATA = './data_products.csv'
CSV_PATH_USER_DATA = './data_users.csv'

def insert_products():
    with open(CSV_PATH_PRODUCT_DATA, 'r', encoding='cp949') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            # main_categories
            if row[1]: # 빈칸 제거 (`` 빈칸의 경우 False니까 빠짐)
                main_categories = row[1]
                if not MainCategory.objects.filter(name = main_categories).exists():
                    # print(main_categories)
                    MainCategory.objects.create(
                        name = main_categories
                    )

            # sub_categories
            if row[3]:
                main_category_id = MainCategory.objects.get(name = main_categories).id
                sub_categories = row[3]
                if SubCategory.objects.filter(name = sub_categories).exists():
                    # print(main_category_id, sub_categories)
                    SubCategory.objects.create(
                        name = sub_categories,
                        main_category_id = main_category_id
                    )

            if row[5] or row[7]:
                sub_category_id = SubCategory.objects.get(name = sub_categories).id
                products = row[5]
                if not Product.objects.filter(name = products).exists():
                    Product.objects.create(
                        name = row[5],
                        price = row
                    )
                    print(sub_category_id, products)




def insert_users():
    with open(CSV_PATH_USER_DATA, 'r', encoding='cp949') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            pass

insert_products()