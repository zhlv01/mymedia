from django.db import models
from django.contrib.auth import get_user_model
from core.models import MediaItem
import secrets

User = get_user_model()


class Share(models.Model):
    """分享链接"""
    media_item = models.ForeignKey(MediaItem, on_delete=models.CASCADE, verbose_name='媒体项目')
    share_code = models.CharField('分享码', max_length=32, unique=True)
    password = models.CharField('访问密码', max_length=32, blank=True)
    expire_at = models.DateTimeField('过期时间', null=True, blank=True)
    view_count = models.IntegerField('访问次数', default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建者')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '分享'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.media_item.title} - {self.share_code}"

    def save(self, *args, **kwargs):
        if not self.share_code:
            self.share_code = secrets.token_urlsafe(16)
        super().save(*args, **kwargs)

    def increment_view(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def get_share_url(self, request=None):
        """获取完整的分享链接"""
        from django.urls import reverse
        return reverse('share:view', kwargs={'code': self.share_code})
