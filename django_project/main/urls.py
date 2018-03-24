from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<document_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<document_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^/add/$', views.vote, name='add_document'),
]