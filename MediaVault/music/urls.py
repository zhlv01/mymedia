from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.music_list, name='list'),
    path('add/', views.music_add, name='add'),
    path('<int:pk>/', views.music_detail, name='detail'),
    path('<int:pk>/edit/', views.music_edit, name='edit'),
    path('<int:pk>/delete/', views.music_delete, name='delete'),
]
