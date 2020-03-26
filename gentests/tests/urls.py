# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from . import views
from django.views.generic import ListView
from tests.models import Test, Task
from .views import SearchResultsView

class TestView(ListView):
    def get_queryset(self):
        return Test.objects.filter(user=self.request.user)

class TaskView(ListView):
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

urlpatterns = [
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^$', views.index, name='index'),
    
    url(r'^start/$', views.index, name='start'),
    url(r'^search/$', SearchResultsView.as_view(queryset=Task.objects.all().order_by("-added_date")), name='search_results'),
    url(r'^test/new/$', views.test_new, name='test_new'),
    url(r'^test/(?P<pk>\d+)/$', views.test_detail, name='test_detail'),
    url(r'^test/(?P<pk>\d+)/edit/$', views.test_edit, name='test_edit'),
    url(r'^test/(?P<pk>\d+)/delete/$', views.test_delete, name='test_delete'),
    url(r'^test/(?P<pk>\d+)/print/$', views.test_print, name='test_print'),
    url(r'^test/(?P<pk>\d+)/variant/new/$', views.variant_new, name='variant_new'),
    url(r'^test/(?P<pk>\d+)/variant/(?P<pk2>\d+)/$', views.variant_detail, name='variant_detail'),
    url(r'^test/(?P<pk>\d+)/variant/(?P<pk2>\d+)/delete/$', views.variant_delete, name='variant_delete'),
    url(r'^test/(?P<pk>\d+)/variant/(?P<pk2>\d+)/print/$', views.variant_print, name='variant_print'),
    url(r'^test/(?P<pk>\d+)/variant/(?P<pk2>\d+)/task/new/$', views.task_new, name='task_new'),
    url(r'^test/(?P<pk>\d+)/variant/(?P<pk2>\d+)/task/(?P<pk3>\d+)/edit/$', views.task_edit, name='task_edit'),
    url(r'^test/(?P<pk>\d+)/variant/(?P<pk2>\d+)/task/(?P<pk3>\d+)/delete/$', views.task_delete, name='task_delete'),
    url(r'^test/list/$', TestView.as_view(queryset=Test.objects.all().order_by("-added_date")[:20], template_name = "tests/test_list.html")),
    url(r'^tasks/list/$', TaskView.as_view(queryset=Task.objects.all().order_by("-added_date")[:20], template_name = "tasks/task_list.html")),
    url(r'^(?P<username>[\w.@+-]+)/$', views.index, name='index'), # why does it need to place last?
]   
