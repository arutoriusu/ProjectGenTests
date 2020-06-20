# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


def get_default_user():
    default_user = User.objects.filter(username="admin").first()
    assert default_user is not None
    return default_user.pk


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Test(models.Model):
    theme_of_test = models.CharField(max_length=30)
    description = models.CharField(max_length=120, blank=True)
    private = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    added_date = models.DateTimeField(default=timezone.now)
    count_of_variants = models.IntegerField(default=0)
    count_of_tasks = models.IntegerField(default=0)
    likes = GenericRelation(Like)

    class Meta:
        verbose_name = "test"
        verbose_name_plural = "tests"

    def __str__(self):
        return f'{self.theme_of_test}'
    
    @property
    def total_likes(self):
        return self.likes.count()


class Variant(models.Model):
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE, related_name='variants', )
    number_of_variant = models.CharField(max_length=2, default="1")
    count_of_tasks = models.IntegerField(default=0)

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
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)
    img = models.ImageField(blank=True, null=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='tasks', default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', default=1)
    tag = models.ManyToManyField(to=Tag, related_name='tasks')
    added_date = models.DateTimeField(default=timezone.now)
    likes = GenericRelation(Like)
    category = models.CharField(max_length=50)

    class Meta:
        verbose_name = "task"
        verbose_name_plural = "tasks"

    def __str__(self):
        return f'{self.question}'

    @property
    def total_likes(self):
        return self.likes.count()
