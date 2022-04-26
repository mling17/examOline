#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from question_bank import models
from question_bank.forms.bootstrap import BootStrapForm


class BankAddModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.QuestionBank
        fields = ['title', 'content', 'cover', 'subject_name']
