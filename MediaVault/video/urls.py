from django.urls import path
from . import views

app_name = 'video'

urlpatterns = [
    path('', views.video_list, name='list'),
    path('add/', views.video_add, name='add'),
    path('<int:pk>/', views.video_detail, name='detail'),
    path('<int:pk>/edit/', views.video_edit, name='edit'),
    path('<int:pk>/delete/', views.video_delete, name='delete'),
]
