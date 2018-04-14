from django.urls import path

from . import views

urlpatterns = [
    path('', views.create, name='create'),
    path('last', views.get_last_id, name='get_last_id')
]
