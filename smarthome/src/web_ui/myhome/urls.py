from django.conf.urls import url

from . import views

app_name = 'myhome'

urlpatterns = [
    url(r'^index/$', views.index, name = 'index'),
    url(r'^index_ajax/$', views.index_ajax, name = 'index_ajax'),
    url(r'^bar1/$', views.bar1, name = 'bar1'),
    url(r'^bar2/$', views.bar2, name = 'bar2'),
    url(r'^bar3/$', views.bar3, name = 'bar3'),
    url(r'^bar4/$', views.bar4, name = 'bar4'),
    url(r'^bar5/$', views.bar5, name = 'bar5'),
]


