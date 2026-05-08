#!/usr/bin/env python
"""
从 SQLite 迁移数据到 MySQL
"""
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediavault.settings')
django.setup()

from django.core import serializers
from django.db import connections

# 要迁移的 models
from users.models import Profile
from core.models import Category, MediaItem
from music.models import Music
from video.models import Video
from notes.models import Note
from share.models import Share
from taggit.models import Tag, TaggedItem

def migrate_model(model, using_from='sqlite3', using_to='default'):
    """迁移单个模型的数据"""
    print(f"正在迁移 {model.__name__}...")
    
    # 从 SQLite 读取
    objects = model.objects.using(using_from).al()
    data = serializers.serialize('json', objects, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    
    # 删除目标数据库中已有数据（可选）
    # model.objects.using(using_to).al().delete()
    
    # 导入到 MySQL
    for obj in serializers.deserialize('json', data, using=using_to):
        obj.save(using=using_to)
    
    print(f"  完成：{objects.count()} 条记录")

# 按顺序迁移
print("=" * 50)
print("开始数据迁移：SQLite -> MySQL")
print("=" * 50)

try:
    # 1. 标签
    migrate_model(Tag)
    
    # 2. 分类
    migrate_model(Category)
    
    # 3. 媒体项
    migrate_model(MediaItem)
    
    # 4. 标签关联
    migrate_model(TaggedItem)
    
    # 5. 各类型具体内容
    migrate_model(Music)
    migrate_model(Video)
    migrate_model(Note)
    
    # 6. 分享
    migrate_model(Share)
    
    # 7. 用户资料
    migrate_model(Profile)
    
    print("=" * 50)
    print("迁移完成！")
    print("=" * 50)
    
except Exception as e:
    print(f"错误：{e}")
    import traceback
    traceback.print_exc()
