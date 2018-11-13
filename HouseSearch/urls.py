from django.urls import path
from HouseSearch import views

urlpatterns = [
    path('', views.house_search_page, name='search_house'),
    path('search/', views.main_search, name='main_search'),
    path('create/', views.house_add_page, name='add_house'),
    path('delete/', views.house_delete, name='delete_house'),
    path('edit/<slug:house_id>/', views.house_edit_page, name='edit_house'),
    path('rate/', views.rate_create, name='house.rate'),
    path('<slug:house_id>/', views.house_page, name='house'),

]

""" path('<slug:user_name>', views.home),
   path('login', views.login),
   path('logout', views.logout),
   path('registrations', views.registr),
"""
