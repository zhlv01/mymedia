from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['media_item', 'get_preview', 'media_item__user', 'media_item__is_public', 'media_item__created_at']
    search_fields = ['media_item__title', 'content']
    list_filter = ['media_item__created_at', 'media_item__is_public', 'media_item__user']
    raw_id_fields = ['media_item']

    def get_preview(self, obj):
        return obj.get_preview()
    get_preview.short_description = '内容预览'

    def media_item__user(self, obj):
        return obj.media_item.user.username
    media_item__user.short_description = '用户'

    def media_item__is_public(self, obj):
        return obj.media_item.is_public
    media_item__is_public.boolean = True
    media_item__is_public.short_description = '公开'
