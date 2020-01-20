# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Test, Variant, Task, Tag


admin.site.register(Test)
admin.site.register(Variant)
admin.site.register(Tag)
admin.site.register(Task)
