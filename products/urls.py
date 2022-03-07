from django.urls import path
from products.views import ProductListView

urlpatterns = [
    path('/product-list', ProductListView.as_view()),
]
