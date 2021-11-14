from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('actors/', views.index, name='actors'),
    path('directors/', views.index, name='directors'),
]
