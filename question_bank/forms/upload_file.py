#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from question_bank import models
from question_bank.forms.bootstrap import BootStrapForm


class UploadFileModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.ImportFile
        fields = ['file']
