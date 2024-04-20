from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('login/', views.app_login, name='app_login'),
    path('logout/', views.app_logout, name='app_logout'),
    path('create_item/', views.create_item, name='create_item'),
    path('search_item/', views.search_item, name='search_item'),
#    path('list/<int:list_id>/add', views.add_item, name='add_item'),
#    path('list/<int:list_id>/remove/<int:item_id>/', views.remove_item, name='remove_item')
]
