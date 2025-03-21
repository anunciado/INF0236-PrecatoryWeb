from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('home', views.home, name='home'),
    path('menu_ente_devedor', views.ente_devedor_menu.as_view(), name='ente_devedor_menu_alias'),
    path('ente_devedor_create/', views.ente_devedor_create.as_view(), name='ente_devedor_create_alias'),
    path('ente_devedor_em_lote_create/', views.ente_devedor_em_lote_create, name='ente_devedor_em_lote_create_alias'),
    path('ente_devedor_update/<int:pk>/', views.ente_devedor_update.as_view(), name='ente_devedor_update_alias'),
    path('ente_devedor_delete/<int:pk>/', views.ente_devedor_delete.as_view(), name='ente_devedor_delete_alias'),
    path('ente_devedor_export_csv/', views.ente_devedor_export_csv, name='ente_devedor_export_csv'),
    path('menu_unidade', views.unidade_menu.as_view(), name='unidade_menu_alias'),
    path('unidade_create/', views.unidade_create.as_view(), name='unidade_create_alias'),
    path('unidade_em_lote_create/', views.unidade_em_lote_create, name='unidade_em_lote_create_alias'),
    path('unidade_update/<int:pk>/', views.unidade_update.as_view(), name='unidade_update_alias'),
    path('unidade_delete/<int:pk>/', views.unidade_delete.as_view(), name='unidade_delete_alias'),
    path('unidade_export_csv/', views.unidade_export_csv, name='unidade_export_csv'),
    path('menu_validacao', views.validacao_menu.as_view(), name='validacao_menu_alias'),
    path('validacao_create/', views.validacao_create.as_view(), name='validacao_create_alias'),
    path('validacao_em_lote_create/', views.validacao_em_lote_create, name='validacao_em_lote_create_alias'),
    path('validacao_update/<int:pk>/', views.validacao_update.as_view(), name='validacao_update_alias'),
    path('validacao_delete/<int:pk>/', views.validacao_delete.as_view(), name='validacao_delete_alias'),
    path('validacao_export_csv/', views.validacao_export_csv, name='validacao_export_csv'),
    path('menu_autuacao', views.autuacao_menu.as_view(), name='autuacao_menu_alias'),
    path('autuacao_create/', views.autuacao_create.as_view(), name='autuacao_create_alias'),
    path('autuacao_em_lote_create/', views.autuacao_em_lote_create, name='autuacao_em_lote_create_alias'),
    path('autuacao_update/<int:pk>/', views.autuacao_update.as_view(), name='autuacao_update_alias'),
    path('autuacao_delete/<int:pk>/', views.autuacao_delete.as_view(), name='autuacao_delete_alias'),
    path('autuacao_export_csv/', views.autuacao_export_csv, name='autuacao_export_csv'),
    path('menu_baixa', views.baixa_menu.as_view(), name='baixa_menu_alias'),
    path('baixa_create/', views.baixa_create.as_view(), name='baixa_create_alias'),
    path('baixa_em_lote_create/', views.baixa_em_lote_create, name='baixa_em_lote_create_alias'),
    path('baixa_update/<int:pk>/', views.baixa_update.as_view(), name='baixa_update_alias'),
    path('baixa_delete/<int:pk>/', views.baixa_delete.as_view(), name='baixa_delete_alias'),
    path('baixa_export_csv/', views.baixa_export_csv, name='baixa_export_csv'),
    path('ia', views.ia_menu, name='ia_menu_alias'),
    path('validacao_modelo_create/', views.validacao_modelo_create, name='validacao_modelo_create_alias'),
    path('train_validacao_model/', views.train_validacao_model, name='train_validacao_model'),
    path('download_validacao_model/', views.download_validacao_model, name='download_validacao_model'),
    path('autuacao_modelo_create/', views.autuacao_modelo_create, name='autuacao_modelo_create_alias'),
    path('train_autuacao_model/', views.train_autuacao_model, name='train_autuacao_model'),
    path('download_autuacao_model/', views.download_autuacao_model, name='download_autuacao_model'),
    path('baixa_modelo_create/', views.baixa_modelo_create, name='baixa_modelo_create_alias'),
    path('train_baixa_model/', views.train_baixa_model, name='train_baixa_model'),
    path('download_baixa_model/', views.download_baixa_model, name='download_baixa_model'),
    path('predicao/', views.index, name='predicao_alias'),
]