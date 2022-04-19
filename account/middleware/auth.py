#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from django.shortcuts import redirect, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from account import models


class UserInfo(object):

    def __init__(self):
        self.user = None
        # self.price_policy = None
        # self.project = None


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):

        """ 如果用户已登录，则request中赋值 """
        request.user_info = UserInfo()
        user_id = request.session.get('user_id', 0)
        user_object = models.User.objects.filter(id=user_id).first()
        request.user_info.user = user_object
        # 白名单：没有登录都可以访问的URL
        """
        1. 获取当用户访问的URL
        2. 检查URL是否在白名单中，如果再则可以继续向后访问，如果不在则进行判断是否已登录
        """
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return
        # 检查用户是否已登录，已登录继续往后走；未登录则返回登录页面。
        if not request.user_info.user:  # 未登录
            return redirect('account:login')
        else:  # 已登录
            # print(not request.user_info.user.mail_valid)
            # print(not request.user_info.user.mail_valid)
            if not request.user_info.user.mail_valid and request.path_info not in settings.WHITE_REGEX_URL_LIST:
                return HttpResponse('邮箱未激活，请先激活邮箱。')
