from django.urls import path

from .views import SignUpView, LogInView, CartView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/login', LogInView.as_view()),
    path('/cart', CartView.as_view()),
]
