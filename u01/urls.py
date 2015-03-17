from django.conf.urls import patterns, url

from u01 import views

urlpatterns = patterns('',
    url(r'^$', views.view),
    url(r'add', views.add),
    url(r'^edit/(?P<username>\w+)/$', views.edit),
    url(r'^delete/(?P<username>\w+)/$', views.delete)
)
