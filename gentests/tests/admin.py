# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Profile, Test, Variant, Task, Tag


admin.site.register(Profile)
admin.site.register(Test)
admin.site.register(Variant)
admin.site.register(Task)
admin.site.register(Tag)
