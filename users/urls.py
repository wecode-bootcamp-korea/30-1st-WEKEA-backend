from django.urls import path

from .views import SignUpView

urlpatterns = [
# http://127.0.0.1:8000/users/signup
    path('/signup', SignUpView.as_view()),
]
