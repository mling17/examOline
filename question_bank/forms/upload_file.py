#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from question_bank import models
from question_bank.forms.bootstrap import BootStrapForm
from django.forms import ValidationError


class UploadFileModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.ImportFile
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1]
        if ext not in ('xls', 'xlsx'):
            raise ValidationError("文件格式不正确，支持格式('xls','xlsx')")
        return file
