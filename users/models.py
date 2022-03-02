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


class OrderedStatus(models.Model):
    status = models.CharField(max_length=30)

    class Meta:
        db_table = 'ordered_statues'


class OrderedProduct(models.Model):
    quantity            = models.IntegerField()
    ordered_status      = models.ForeignKey('OrderedStatus', on_delete=models.CASCADE)
    user                = models.ForeignKey('User', on_delete=models.CASCADE)
    product_information = models.ForeignKey('products.ProductInformation', on_delete=models.CASCADE)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ordered_products'


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
    comment    = models.TextField() # 길이제한을 없애기 위하여 TextField 사용
    user       = models.ForeignKey('User', on_delete=models.PROTECT) # 유저가 탈퇴했을 경우에도 리뷰는 변함이 없어야하기 때문에 PROTECT 사용
    product    = models.ForeignKey('products.Product', on_delete=models.CASCADE) # 제품이 삭제된 경우엔 리뷰도 같이 사라지기 때문에 CASCADE 사용
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'