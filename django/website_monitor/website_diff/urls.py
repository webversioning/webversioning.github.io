from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^check/$', views.check_for_changes, name = 'check_for_changes'),
]