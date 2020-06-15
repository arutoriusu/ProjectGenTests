# -*- coding: utf-8 -*-

from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Test, Variant, Task, Tag, Like



class TaskAdmin(SummernoteModelAdmin):
    summernote_fields = ('question','answer',)
    list_display = ['text_format']
    
    def text_format(self, obj):
        return mark_safe(obj.question)
    
    text_format.short_description = 'Задачи'

admin.site.register(Test)
admin.site.register(Variant)
admin.site.register(Tag)
admin.site.register(Task, TaskAdmin)
admin.site.register(Like)
