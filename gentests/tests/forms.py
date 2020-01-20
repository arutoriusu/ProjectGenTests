from django import forms
from .models import Test, Variant, Task, Tag
from django.contrib.auth.models import User


class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ['theme_of_test', ]


class VariantForm(forms.ModelForm):

    class Meta:
        model = Variant
        fields = ['number_of_variants', ]


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['question', 'answer', ]


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['name_tag', ]


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтори пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
