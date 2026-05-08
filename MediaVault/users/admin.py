from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile
from core.models import MediaItem


# 先注销原有的 User Admin
admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = '用户资料'


class UserMediaStats:
    """用户媒体统计Mixin"""
    def music_count(self, obj):
        return MediaItem.objects.filter(user=obj, media_type='music').count()
    music_count.short_description = '音乐'

    def video_count(self, obj):
        return MediaItem.objects.filter(user=obj, media_type='video').count()
    video_count.short_description = '视频'

    def note_count(self, obj):
        return MediaItem.objects.filter(user=obj, media_type='note').count()
    note_count.short_description = '笔记'

    def total_count(self, obj):
        return MediaItem.objects.filter(user=obj).count()
    total_count.short_description = '总计'

    def public_count(self, obj):
        return MediaItem.objects.filter(user=obj, is_public=True).count()
    public_count.short_description = '公开'


@admin.register(User)
class UserAdmin(BaseUserAdmin, UserMediaStats):
    list_display = list(BaseUserAdmin.list_display) + ['music_count', 'video_count', 'note_count', 'public_count', 'date_joined']
    list_select_related = ['profile']

    fieldsets = list(BaseUserAdmin.fieldsets) + [
        ('媒体统计', {'fields': ('music_count', 'video_count', 'note_count', 'public_count'), 'classes': ('collapse',)}),
    ]

    inlines = [ProfileInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar_preview', 'bio', 'website', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'bio']
    list_select_related = ['user']

    def avatar_preview(self, obj):
        if obj.avatar:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 50%;">', obj.avatar.url)
        return '-'
    avatar_preview.short_description = '头像'
