from django.urls import path
from Chat import views

urlpatterns = [
    path('', views.chat_list),
    path('create_message/', views.create_message, name='create_message'),
    path('chats/<str:chat_slug>/', views.chat_block),

]
# path('<str:room_name>/', views.chat_page, name='room'),
# path('', views.chat_list_page),
