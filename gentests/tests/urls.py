from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^start/$', views.index, name='start'),
    url(r'^test/new/$', views.test_new, name='test_new')
]
