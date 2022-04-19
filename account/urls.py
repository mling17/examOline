"""recite_words URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
import account.views as views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('email_active/', views.email_active, name='email_active'),
    path('send_change_password_mail/', views.send_change_password_mail, name='send_change_password_mail'),
    path('change_password/', views.change_password, name='change_password'),
    path('forget/', views.forget, name='forget'),
    path('hello/', views.hello, name='hello'),
    re_path(r'image/code/$', views.image_code, name='image_code'),
]
