from django.urls import path
from UserProfile import views

urlpatterns = [

    path('note/create/', views.note_create_page, name='user_profile.note_create'),
    path('note/delete/', views.delete_note, name='note_delete'),
    path('note/edit/<slug:note_id>/', views.note_edit_page, name='note_edit'),
    path('note/<slug:note_id>/', views.note_page, name='note'),
    path('<slug:user_id>/load_notes/', views.load_notes, name='load_notes'),
    path('<slug:user_id>/', views.home, name='home'),

]


""" path('<slug:user_name>', views.home),
   path('login', views.login),
   path('logout', views.logout),
   path('registrations', views.registr),
"""