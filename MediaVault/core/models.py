from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from taggit.managers import TaggableManager

User = get_user_model()


class Category(models.Model):
    """分类"""
    name = models.CharField('分类名称', max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    color = models.CharField('颜色', max_length=7, default='#007bff')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        unique_together = ['name', 'user']
        ordering = ['name']

    def __str__(self):
        return self.name


class MediaItem(models.Model):
    """媒体项目基类"""
    MEDIA_TYPES = (
        ('music', '音乐'),
        ('video', '视频'),
        ('note', '笔记'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    title = models.CharField('标题', max_length=255)
    description = models.TextField('描述', blank=True)
    cover_image = models.ImageField('封面图', upload_to='covers/%Y/%m/', blank=True, null=True)
    media_type = models.CharField('媒体类型', max_length=10, choices=MEDIA_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='分类', blank=True, null=True)
    tags = TaggableManager('标签', blank=True)
    is_public = models.BooleanField('公开', default=False)
    view_count = models.IntegerField('浏览次数', default=0)
    like_count = models.IntegerField('喜欢次数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '媒体项目'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.media_type == 'music':
            try:
                return reverse('music:detail', kwargs={'pk': self.music.pk})
            except Exception:
                return reverse('music:list')
        elif self.media_type == 'video':
            try:
                return reverse('video:detail', kwargs={'pk': self.video.pk})
            except Exception:
                return reverse('video:list')
        elif self.media_type == 'note':
            try:
                return reverse('notes:detail', kwargs={'pk': self.note.pk})
            except Exception:
                return reverse('notes:list')
        return reverse('dashboard')

    def increment_view(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
