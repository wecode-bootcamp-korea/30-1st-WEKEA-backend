from django.urls import path
from products.views import ProductListView,SubcategoryListView

urlpatterns = [
    path('/product-list', ProductListView.as_view()),
    path('/sub-category-list', SubcategoryListView.as_view()),
]