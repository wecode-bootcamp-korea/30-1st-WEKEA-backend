from django.db import models

class Product(models.Model):
    name         = models.CharField(max_length=50)
    price        = models.DecimalField(max_digits=12, decimal_places=2)
    description  = models.TextField()
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    discount     = models.ForeignKey('Discount', on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'


class Discount(models.Model):
    rate = models.IntegerField(default=0)
    type = models.CharField()

    class Meta:
        db_table = 'discounts'


class Image(models.Model):
    image_url = models.CharField(max_length=200)
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'images'


class SubCategory(models.Model):
    name          = models.CharField(max_length=50)
    main_category = models.ForeignKey('MainCategory', on_delete=models.CASCADE)
    description   = models.TextField()
    image_url     = models.CharField(max_length=200)

    class Meta:
        db_table = 'sub_categories'


class MainCategory(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'main_categories'


class ProductInformation(models.Model):
    product         = models.ForeignKey('Product', on_delete=models.CASCADE)
    store           = models.ForeignKey('Store', on_delete=models.CASCADE)
    color           = models.ForeignKey('Color', on_delete=models.CASCADE)
    size            = models.ForeignKey('Size', on_delete=models.CASCADE)
    remaining_stock = models.IntegerField()
    
    class Meta:
        db_table = 'product_informations'


class Store(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'stores'


class Color(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'colors'


class Size(models.Model):
    size = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'sizes'





