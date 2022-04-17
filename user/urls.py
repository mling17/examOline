from django.urls import path
from user.views import register

urlpatterns = [
    path('register/', register, name='register'),
]
