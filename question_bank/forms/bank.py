#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from question_bank import models
from question_bank.forms.bootstrap import BootStrapForm
from ckeditor.fields import RichTextFormField


class BankAddModelForm(BootStrapForm, forms.ModelForm):
    # def __init__(self, request, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.request = request

    class Meta:
        model = models.QuestionBank
        fields = ['title', 'content', 'cover', 'subject_name']
