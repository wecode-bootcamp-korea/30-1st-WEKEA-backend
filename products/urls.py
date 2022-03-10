from django.urls import path
from products.views import ProductListView,ProductDetailView

urlpatterns = [
    path('/product', ProductListView.as_view()),
    path("/<int:product_id>", ProductDetailView.as_view())
]