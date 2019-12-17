from django import forms
from .models import Profile, Test, Variant, Task, Tag


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
