# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


def get_default_user():
    default_user = User.objects.filter(username="admin").first()
    assert default_user is not None
    return default_user.pk


class Test(models.Model):
    theme_of_test = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    added_date = models.DateTimeField(default=timezone.now)
    count_of_variants = models.IntegerField(default=0)
    count_of_tasks = models.IntegerField(default=0)
    category = models.CharField(max_length=50, default='Алгебра')

    class Meta:
        verbose_name = "test"
        verbose_name_plural = "tests"

    def __str__(self):
        return f'{self.theme_of_test}'


class Variant(models.Model):
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE, related_name='variants', )
    number_of_variant = models.CharField(max_length=2, default="1")

    class Meta:
        verbose_name = "variant"
        verbose_name_plural = "variants"


class Tag(models.Model):
    name_tag = models.CharField(max_length=30)
    
    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def __str__(self):
        return f'{self.name_tag}'


class Task(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    img = models.ImageField(blank=True, null=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='tasks', default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', default=1)
    tag = models.ManyToManyField(to=Tag, related_name='tasks')
    added_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "task"
        verbose_name_plural = "tasks"

    def __str__(self):
        return f'{self.question}'
