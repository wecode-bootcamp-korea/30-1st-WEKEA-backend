from django.urls import path
from products.views import ProductListView

urlpatterns = [
    path('/product', ProductListView.as_view()),
]