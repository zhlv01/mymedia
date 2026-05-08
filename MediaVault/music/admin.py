from django.contrib import admin
from .models import Music


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['media_item', 'artist', 'album', 'get_duration', 'media_item__user', 'media_item__is_public']
    search_fields = ['media_item__title', 'artist', 'album']
    list_filter = ['media_item__created_at', 'media_item__is_public', 'media_item__user']
    raw_id_fields = ['media_item']

    def get_duration(self, obj):
        return obj.get_duration_display()
    get_duration.short_description = '时长'

    def media_item__user(self, obj):
        return obj.media_item.user.username
    media_item__user.short_description = '用户'

    def media_item__is_public(self, obj):
        return obj.media_item.is_public
    media_item__is_public.boolean = True
    media_item__is_public.short_description = '公开'
