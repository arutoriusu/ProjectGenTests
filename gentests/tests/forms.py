# -*- coding: utf-8 -*-

from django_summernote.widgets import SummernoteWidget
from captcha.fields import CaptchaField
from django import forms
from .models import Test, Variant, Task, Tag
from django.contrib.auth.models import User 

MATH_CHOICES= [
    ('Арифметика', 'Арифметика'),
    ('Алгебраэлементарнаяматематика', 'Алгебра (элементарная математика)'),
    ('Геометрия', 'Геометрия'),
    ('Теорияэлементарныхфункцийиэлементы анализа', 'Теория элементарных функций и элементы анализа'),
    ('Математическийанализ', 'Математический анализ'),
    ('Алгебравысшаяматематика)', 'Алгебра (высшая математика)'),
    ('Аналитическаягеометрия', 'Аналитическая геометрия'),
    ('Линейнаяалгебраигеометрия', 'Линейная алгебра и геометрия'),
    ('Дискретнаяматематика', 'Дискретная математика'),
    ('Математическаялогика', 'Математическая логика'),
    ('Дифференциальныеуравнения', 'Дифференциальные уравнения'),
    ('Дифференциальнаягеометрия', 'Дифференциальная геометрия'),
    ('Топология', 'Топология'),
    ('Функциональныйанализиинтегральныеуравнения', 'Функциональный анализ и интегральные уравнения'),
    ('Теорияфункцийкомплексногопеременного', 'Теория функций комплексного переменного'),
    ('Уравнениясчастнымипроизводными', 'Уравнения с частными производными'),
    ('Теориявероятностей', 'Теория вероятностей'),
    ('Математическаястатистика', 'Математическая статистика'),
    ('Теорияслучайныхпроцессов', 'Теория случайных процессов'),
    ('Вариационноеисчислениеиметодыоптимизации', 'Вариационное исчисление и методы оптимизации'),
    ('Численныеметоды', 'Численные методы'),
    ('Теориячисел', 'Теория чисел'),
    ]

class TestForm(forms.ModelForm):
    theme_of_test = forms.CharField(label=("Название"),)
    description = forms.CharField(label=("Описание"),)

    class Meta:
        model = Test
        fields = ['theme_of_test', 'description', 'private', ]


class TaskForm(forms.ModelForm):
    question = forms.CharField(widget=forms.Textarea)
    answer = forms.CharField(widget=forms.Textarea)
    category = forms.CharField(label='Выберите категорию для задачи', widget=forms.Select(choices=MATH_CHOICES))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget.attrs.update(id='testbox')
        self.fields['answer'].widget.attrs.update(id='testbox2')

    class Meta:
        model = Task
        fields = ['question', 'answer', 'category', ]
        # widgets = {
        #     'question': SummernoteWidget(),
        #     'answer': SummernoteWidget(),
        # }


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['name_tag', ]


class UserRegistrationForm(forms.ModelForm):
    captcha = CaptchaField(label=("Защита от робота"),)
    password = forms.CharField(label=("Пароль"),
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','password',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']
