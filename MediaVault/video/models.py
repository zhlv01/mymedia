from django.db import models
from core.models import MediaItem


class Video(models.Model):
    """视频"""
    media_item = models.OneToOneField(MediaItem, on_delete=models.CASCADE, related_name='video')
    duration = models.IntegerField('时长（秒）', blank=True, null=True)
    file = models.FileField('视频文件', upload_to='video/%Y/%m/', blank=True, null=True)
    external_url = models.URLField('外部链接', blank=True, help_text='YouTube/B站/抖音等外部链接')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name
        ordering = ['-media_item__created_at']

    def __str__(self):
        return self.media_item.title

    def get_absolute_url(self):
        return self.media_item.get_absolute_url()

    def get_duration_display(self):
        if self.duration:
            minutes = self.duration // 60
            seconds = self.duration % 60
            return f"{minutes}:{seconds:02d}"
        return "0:00"
