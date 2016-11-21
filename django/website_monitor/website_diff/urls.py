from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^check/$', views.check_for_changes, name = 'check_for_changes'),
    url(r'^get_domains/$', views.get_domains, name = 'get_domains'),
    url(r'^get_diff/$', views.get_diff, name = 'get_diff'),
]