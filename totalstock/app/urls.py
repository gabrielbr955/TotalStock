from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('login/', views.app_login, name='app_login'),
    path('logout/', views.app_logout, name='app_logout'),
    path('create_item/', views.create_item, name='create_item'),
    path('search_item/', views.search_item, name='search_item'),
    path('issuance/<int:stock_id>/', views.issuance, name='issuance'),
    path('receiving/', views.receiving, name='receiving'),
    path('adjust_stock/<int:stock_id>/', views.adjust_stock, name='adjust_stock'),
    path('manage_users/', views.manage_users, name='manage_users'),
]