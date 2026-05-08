from django.urls import path
from . import views

app_name = 'share'

urlpatterns = [
    path('s/<str:code>/', views.share_view, name='view'),
    path('create/<int:media_id>/', views.share_create, name='create'),
    path('delete/<int:pk>/', views.share_delete, name='delete'),
    path('my-shares/', views.my_shares, name='my_shares'),
    path('quick/<int:media_id>/', views.quick_public_share, name='quick'),
    path('toggle/<int:media_id>/', views.toggle_public_share, name='toggle'),
]
