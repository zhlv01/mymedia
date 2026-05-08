from django.db import models
from core.models import MediaItem


class Note(models.Model):
    """笔记"""
    media_item = models.OneToOneField(MediaItem, on_delete=models.CASCADE, related_name='note')
    content = models.TextField('内容', blank=True)
    content_type = models.CharField('内容类型', max_length=20, default='markdown')

    class Meta:
        verbose_name = '笔记'
        verbose_name_plural = verbose_name
        ordering = ['-media_item__created_at']

    def __str__(self):
        return self.media_item.title

    def get_absolute_url(self):
        return self.media_item.get_absolute_url()

    def get_preview(self):
        """获取预览内容"""
        if len(self.content) > 200:
            return self.content[:200] + '...'
        return self.content
