from django.contrib import admin
from .models import Tag, Task, Test, Variant

admin.site.register(Tag)
admin.site.register(Task)
admin.site.register(Test)
admin.site.register(Variant)
