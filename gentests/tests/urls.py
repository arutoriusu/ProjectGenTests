from django.conf.urls import url, include
from . import views
from django.views.generic import ListView
from tests.models import Test

class TestView(ListView):
    def get_queryset(self):
        return Test.objects.filter(user=self.request.user)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<username>[\w.@+-]+)/$', views.index, name='index'),
    url(r'^start/$', views.index, name='start'),
    url(r'^test/new/$', views.test_new, name='test_new'),
    url(r'^test/(?P<pk>\d+)/$', views.test_detail, name='test_detail'),
    url(r'^test/(?P<pk>\d+)/task/new/$', views.task_new, name='task_new'),
    url(r'^registration/', views.registration, name='registration'),
    url(r'^test/list/$', TestView.as_view(queryset=Test.objects.all().order_by("-added_date")[:20], template_name = "tests/test_list.html")),
]   
