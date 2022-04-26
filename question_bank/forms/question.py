#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
from django import forms
from question_bank import models
from question_bank.forms.bootstrap import BootStrapForm


class QuestionAddModelForm(BootStrapForm, forms.ModelForm):
    attr = {
        'class': 'form-control',
        'placeholder': "请输入解析",
        'cols': 40,
        'rows': 2,
        'maxlength': 1024
    }
    analysis = forms.CharField(label='解析', widget=forms.Textarea(attrs=attr), required=True)

    class Meta:
        model = models.Question
        fields = ['sort_num', 'type', 'title', 'analysis']


class QuestionEditModelForm(BootStrapForm, forms.ModelForm):
    attr = {
        'class': 'form-control',
        'placeholder': "请输入解析",
        'cols': 40,
        'rows': 2,
        'maxlength': 1024
    }
    analysis = forms.CharField(label='解析', widget=forms.Textarea(attrs=attr), required=True)
    type = forms.CharField(label='hide', widget=forms.HiddenInput)

    class Meta:
        model = models.Question
        exclude = ['user_id', 'is_valid']
