from django.contrib import admin
from .models import Share


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ['media_item', 'share_code', 'created_by', 'view_count', 'created_at', 'expire_at']
    search_fields = ['media_item__title', 'share_code']
    list_filter = ['created_at', 'expire_at']
    readonly_fields = ['share_code']
    raw_id_fields = ['media_item', 'created_by']
    date_hierarchy = 'created_at'
