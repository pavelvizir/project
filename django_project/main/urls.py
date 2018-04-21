from django.urls import path
from django.conf.urls import url
from . import views
from .views import MyView

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^data/(?P<id>[0-9]+)/$', views.detail, name='detail'),
#    url(r'^(?P<document_id>[0-9]+)/$', views.detail2, name='detail2'),
#    url(r'^(?P<document_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^data/$', views.index_data, name='index_data'),
    url('api/', MyView.as_view(), name='my-view'),
    path('', views.create, name='create'),
    path('last', views.get_last_id, name='get_last_id'),
    path('search', views.full_text_search, name='full_text_search')
]
