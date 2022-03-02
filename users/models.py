from django.db import models

class User(models.Model):
    full_name    = models.CharField(max_length=40)
    email        = models.EmailField(max_length=50, unique=True)
    password     = models.CharField(max_length=100)
    membership   = models.BooleanField(default=False)
    address      = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    gender       = models.ForeignKey('Gender', on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'


class Gender(models.Model):
    gender = models.CharField(max_length=10)

    class Meta:
        db_table = 'genders'


class OrderStatus(models.Model):
    status = models.CharField(max_length=30)

    class Meta:
        db_table = 'order_status'


class OrderProduct(models.Model):
    quantity            = models.IntegerField()
    order_status        = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)
    user                = models.ForeignKey('User', on_delete=models.CASCADE)
    product_information = models.ForeignKey('products.ProductInformation', on_delete=models.CASCADE)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_products'


class Cart(models.Model):
    quantity            = models.IntegerField()
    user                = models.ForeignKey('User', on_delete=models.CASCADE)
    product_information = models.ForeignKey('products.ProductInformation', on_delete=models.CASCADE)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'


class Review(models.Model):
    rating     = models.IntegerField()
    comment    = models.TextField()
    user       = models.ForeignKey('User', on_delete=models.PROTECT)
    product    = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'