from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recherche/', views.recherche, name='recherche'),
    path('compute/', views.compute, name='compute'),
    path('ajax/idsearch/', views.id_search_ajax, name='id_search_ajax'),
    path('ajax/mass/search/', views.mass_search, name='mass_search'),


]