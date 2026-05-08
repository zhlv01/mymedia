from django.contrib import admin
from .models import Category, MediaItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name']


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'media_type', 'category', 'is_public', 'view_count', 'created_at']
    list_filter = ['media_type', 'is_public', 'category', 'created_at', 'user']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
