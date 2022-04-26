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
from question_bank.views import bank
from question_bank.views import question

urlpatterns = [
    # 题库
    path('bank_list/', bank.bank_list, name='bank_list'),
    path('bank_add/', bank.bank_add, name='bank_add'),
    re_path(r'bank_edit/(?P<pk>\d+)/$', bank.edit, name='bank_edit'),
    re_path(r'bank_delete/(?P<pk>\d+)/$', bank.delete, name='bank_delete'),
    # 题
    path('question_list/', question.question_list, name='question_list'),
    re_path(r'question_add/', question.question_add, name='question_add'),
    re_path(r'question_edit/(?P<pk>\d+)/$', question.question_change, name='question_edit'),
    path(r'get_question_options/', question.get_question_options, name='get_question_options'),
    re_path(r'question_delete/(?P<pk>\d+)/$', question.question_delete, name='question_delete'),
    path('import_question/', bank.import_question, name='import_question'),
]
