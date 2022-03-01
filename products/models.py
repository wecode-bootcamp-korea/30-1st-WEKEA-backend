from django.db import models

class Product(models.Model):
    name         = models.CharField(max_length=50)
    price        = models.DecimalField(max_digits=None, decimal_places=2)
    discription  = models.TextField()
    sub_category = models.ForeignKey('Sub_category', on_delete=models.CASCADE)

    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'


class Image(models.Model):
    image_url = models.CharField(max_length=200)
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'images'


class Sub_category(models.Model):
    name          = models.CharField(max_length=50)
    main_category = models.ForeignKey('Main_category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'


class Main_category(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'main_categories'


class Product_information(models.Model):
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