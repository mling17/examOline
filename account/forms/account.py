#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings

from account import models
from account.forms.forms import BootStrapForm
from account.utils import encrypt


class RegisterModelForm(BootStrapForm, forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    password = forms.CharField(
        label='密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "密码长度不能小于8个字符",
            'max_length': "密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        label='重复密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "重复密码长度不能小于8个字符",
            'max_length': "重复密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput())

    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput())

    class Meta:
        model = models.User
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']

    def clean_username(self):
        username = self.cleaned_data['username']
        exists = models.User.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
            # self.add_error('username','用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = models.User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 加密 & 返回
        p = encrypt.md5(pwd)
        print(p)
        return p

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = encrypt.md5(self.cleaned_data['confirm_password'])
        if pwd != confirm_pwd:
            raise ValidationError('两次密码不一致')
        return confirm_pwd

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.User.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已注册')
        return mobile_phone

    def clean_code(self):
        """ 钩子 图片验证码是否正确？ """
        # 读取用户输入的yanzhengm
        code = self.cleaned_data['code']
        # 去session获取自己的验证码
        session_code = self.request.session.get('image_code')
        if not session_code:
            raise ValidationError('验证码已过期，请重新获取')
        if code.strip().upper() != session_code.strip().upper():
            raise ValidationError('验证码输入错误')
        return code


class LoginForm(BootStrapForm, forms.Form):
    username = forms.CharField(label='邮箱或手机号')
    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True))
    code = forms.CharField(label='图片验证码')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 加密 & 返回
        return encrypt.md5(pwd)

    def clean_code(self):
        """ 钩子 图片验证码是否正确？ """
        # 读取用户输入的yanzhengm
        code = self.cleaned_data['code']
        # 去session获取自己的验证码
        session_code = self.request.session.get('image_code')
        if not session_code:
            raise ValidationError('验证码已过期，请重新获取')
        if code.strip().upper() != session_code.strip().upper():
            raise ValidationError('验证码输入错误')
        return code


class ChangePasswordForm(BootStrapForm, forms.Form):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    password = forms.CharField(
        label='新密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "密码长度不能小于8个字符",
            'max_length': "密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        label='重复密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "重复密码长度不能小于8个字符",
            'max_length': "重复密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput())

    # code = forms.CharField(
    #     label='验证码',
    #     widget=forms.TextInput())

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 加密 & 返回
        p = encrypt.md5(pwd)
        return p

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = encrypt.md5(self.cleaned_data['confirm_password'])
        if pwd != confirm_pwd:
            raise ValidationError('两次密码不一致')
        return confirm_pwd

    # def clean_code(self):
    #     """ 钩子 图片验证码是否正确？ """
    #     # 读取用户输入的yanzhengm
    #     code = self.cleaned_data['code']
    #     # 去session获取自己的验证码
    #     session_code = self.request.session.get('image_code')
    #     if not session_code:
    #         raise ValidationError('验证码已过期，请重新获取')
    #     if code.strip().upper() != session_code.strip().upper():
    #         raise ValidationError('验证码输入错误')
    #     return code


class ForgetPasswordForm(BootStrapForm, forms.Form):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    email = forms.EmailField(label='邮箱', required=True)
    password = forms.CharField(
        label='新密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "密码长度不能小于8个字符",
            'max_length': "密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        label='重复密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "重复密码长度不能小于8个字符",
            'max_length': "重复密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = models.User.objects.filter(email=email).exists()
        if not exists:
            raise ValidationError('邮箱不存在')
        return email

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 加密 & 返回
        p = encrypt.md5(pwd)
        return p

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = encrypt.md5(self.cleaned_data['confirm_password'])
        if pwd != confirm_pwd:
            raise ValidationError('两次密码不一致')
        return confirm_pwd
    # def clean_code(self):
    #     """ 钩子 图片验证码是否正确？ """
    #     # 读取用户输入的yanzhengm
    #     code = self.cleaned_data['code']
    #     # 去session获取自己的验证码
    #     session_code = self.request.session.get('image_code')
    #     if not session_code:
    #         raise ValidationError('验证码已过期，请重新获取')
    #     if code.strip().upper() != session_code.strip().upper():
    #         raise ValidationError('验证码输入错误')
    #     return code
