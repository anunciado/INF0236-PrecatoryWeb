from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index1'),
    path('grafico', views.grafico, name='grafico'),
    path('menu_ente_devedor', views.ente_devedor_menu.as_view(), name='ente_devedor_menu_alias'),
    path('ente_devedor_create/', views.ente_devedor_create.as_view(), name='ente_devedor_create_alias'),
    path('ente_devedor_em_lote_create/', views.ente_devedor_em_lote_create, name='ente_devedor_em_lote_create_alias'),
    path('ente_devedor_update/<int:pk>/', views.ente_devedor_update.as_view(), name='ente_devedor_update_alias'),
    path('ente_devedor_delete/<int:pk>/', views.ente_devedor_delete.as_view(), name='ente_devedor_delete_alias'),
    path('menu_unidade', views.unidade_menu.as_view(), name='unidade_menu_alias'),
    path('unidade_create/', views.unidade_create.as_view(), name='unidade_create_alias'),
    path('unidade_em_lote_create/', views.unidade_em_lote_create, name='unidade_em_lote_create_alias'),
    path('unidade_update/<int:pk>/', views.unidade_update.as_view(), name='unidade_update_alias'),
    path('unidade_delete/<int:pk>/', views.unidade_delete.as_view(), name='unidade_delete_alias'),
    ]