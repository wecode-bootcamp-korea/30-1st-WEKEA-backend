from django.urls import path
from products.views import ProductListView,ProductDetailView,UpdateSubCategoryView

urlpatterns = [
    path('/product', ProductListView.as_view()),
    path("/<int:product_id>", ProductDetailView.as_view()),
    path('/default-options', UpdateSubCategoryView.as_view())
]