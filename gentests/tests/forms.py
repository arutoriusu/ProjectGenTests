# -*- coding: utf-8 -*-

from django_summernote.widgets import SummernoteWidget
from captcha.fields import CaptchaField
from django import forms
from .models import Test, Variant, Task, Tag
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 


class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ['theme_of_test', ]


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['question', 'answer', ]
        widgets = {
            'question': SummernoteWidget(),
            'answer': SummernoteWidget(),
        }


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['name_tag', ]


class UserRegistrationForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username','password',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']
