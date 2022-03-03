from django.urls import path, include

urlpatterns = [
# http://127.0.0.1:8000/users
    path('users', include('users.urls')),
# http://127.0.0.1:8000/products
    # path('products', include('products.urls'))
]
