from django.urls import path
from Chat import views

urlpatterns = [
    path('', views.chat_list),
    path('create/convers/', views.create_conversation, name='chat.create_conversation'),
    path('create/', views.create_chat, name='chat.create_chat'),
    path('add/members/<slug:chat_slug>/', views.add_members, name='chat.add_members'),
    path('load/users/', views.load_users, name='chat.load_users'),
    path('get/user/', views.get_user, name='chat.get_user'),
    path('create_message/', views.create_message, name='create_message'),
    path('chats/<str:chat_slug>/', views.chat_block),

]
# path('<str:room_name>/', views.chat_page, name='room'),
# path('', views.chat_list_page),
