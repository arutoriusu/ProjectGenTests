# -*- coding: utf-8 -*-

from django_summernote.widgets import SummernoteWidget
from captcha.fields import CaptchaField
from django import forms
from .models import Test, Variant, Task, Tag
from django.contrib.auth.models import User 

MATH_CHOICES= [
    ('Арифметика', 'Арифметика'),
    ('Алгебра (элементарная математика)', 'Алгебра (элементарная математика)'),
    ('Геометрия', 'Геометрия'),
    ('Теория элементарных функций и элменты анализа', 'Теория элементарных функций и элменты анализа'),
    ('Математический анализ', 'Математический анализ'),
    ('Алгебра (высшая математика)', 'Алгебра (высшая математика)'),
    ('Аналитическая геометрия', 'Аналитическая геометрия'),
    ('Линейная алгебра и геометрия', 'Линейная алгебра и геометрия'),
    ('Дискретная математика', 'Дискретная математика'),
    ('Математическая логика', 'Математическая логика'),
    ('Дифференциальные уравнения', 'Дифференциальные уравнения'),
    ('Дифференциальная геометрия', 'Дифференциальная геометрия'),
    ('Топология', 'Топология'),
    ('Функциональный анализ и интегральные уравнения', 'Функциональный анализ и интегральные уравнения'),
    ('Теория функций комплексного переменного', 'Теория функций комплексного переменного'),
    ('Уравнения с частными производными', 'Уравнения с частными производными'),
    ('Теория вероятностей', 'Теория вероятностей'),
    ('Математическая статистика', 'Математическая статистика'),
    ('Теория случайных процессов', 'Теория случайных процессов'),
    ('Вариационное исчисление и методы оптимизации', 'Вариационное исчисление и методы оптимизации'),
    ('Методы вычислений, т.е.численные методы', 'Методы вычислений, т.е.численные методы'),
    ('Теория чисел', 'Теория чисел'),
    ]

class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ['theme_of_test', ]


class TaskForm(forms.ModelForm):

    category = forms.CharField(label='Выберите категорию для задачи', widget=forms.Select(choices=MATH_CHOICES))

    class Meta:
        model = Task
        fields = ['question', 'answer', 'category',]
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
