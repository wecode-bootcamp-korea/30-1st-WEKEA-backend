from django.urls import path

from .views import ProductDetailView

urlpatterns = [
    path("/detail/<int:product_id>", ProductDetailView.as_view()),
]