from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recherche/', views.recherche, name='recherche'),
    path('compute/', views.compute, name='compute'),
    path('idsearch/', views.idsearch, name='idsearch'),

]