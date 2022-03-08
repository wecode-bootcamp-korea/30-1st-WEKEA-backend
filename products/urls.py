from django.urls import path

from .views import ProductDetailView

urlpatterns = [
    path("/detail", ProductDetailView.as_view()),
]