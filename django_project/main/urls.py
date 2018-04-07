from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^data/(?P<id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<document_id>[0-9]+)/$', views.detail2, name='detail2'),
    # url(r'^(?P<document_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^data/$', views.index_data, name='index_data'),
]