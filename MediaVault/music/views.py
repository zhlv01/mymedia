from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Music
from .forms import MusicForm
from core.models import MediaItem
from mutagen import File as MutagenFile
import os


@login_required
def music_list(request):
    """音乐列表"""
    music_items = Music.objects.filter(media_item__user=request.user).select_related('media_item')
    
    # 按标签筛选
    tag = request.GET.get('tag')
    if tag:
        music_items = music_items.filter(media_item__tags__name=tag)
    
    # 按分类筛选
    category = request.GET.get('category')
    if category:
        music_items = music_items.filter(media_item__category__id=category)
    
    context = {
        'music_items': music_items,
        'tag_filter': tag,
        'category_filter': category,
    }
    return render(request, 'music/list.html', context)


@login_required
def music_detail(request, pk):
    """音乐详情"""
    music = get_object_or_404(Music, pk=pk, media_item__user=request.user)
    music.media_item.increment_view()
    return render(request, 'music/detail.html', {'music': music})


@login_required
def music_add(request):
    """添加音乐"""
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            # 创建 MediaItem
            media_item = MediaItem.objects.create(
                user=request.user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                cover_image=form.cleaned_data.get('cover_image'),
                category=form.cleaned_data.get('category'),
                media_type='music',
                is_public=form.cleaned_data.get('is_public', False)
            )
            
            # 添加标签
            tags_str = form.cleaned_data.get('tags', '')
            if tags_str:
                tag_list = [t.strip() for t in tags_str.split(',') if t.strip()]
                media_item.tags.add(*tag_list)
            
            # 创建 Music
            music = form.save(commit=False)
            music.media_item = media_item
            
            # 如果上传了文件，尝试获取时长
            if form.cleaned_data.get('file'):
                try:
                    audio_file = MutagenFile(form.cleaned_data['file'].temporary_file_path())
                    if audio_file and hasattr(audio_file, 'info') and audio_file.info.length:
                        music.duration = int(audio_file.info.length)
                except:
                    pass
            
            music.save()
            
            messages.success(request, '音乐添加成功！')
            return redirect('music:detail', pk=music.pk)
    else:
        form = MusicForm(user=request.user)
    
    return render(request, 'music/form.html', {'form': form, 'title': '添加音乐'})


@login_required
def music_edit(request, pk):
    """编辑音乐"""
    music = get_object_or_404(Music, pk=pk, media_item__user=request.user)
    
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES, instance=music, user=request.user)
        if form.is_valid():
            # 更新 MediaItem
            media_item = music.media_item
            media_item.title = form.cleaned_data['title']
            media_item.description = form.cleaned_data['description']
            if form.cleaned_data.get('cover_image'):
                media_item.cover_image = form.cleaned_data['cover_image']
            media_item.category = form.cleaned_data.get('category')
            media_item.is_public = form.cleaned_data.get('is_public', False)
            media_item.save()
            
            # 更新标签
            tags_str = form.cleaned_data.get('tags', '')
            media_item.tags.clear()
            if tags_str:
                tag_list = [t.strip() for t in tags_str.split(',') if t.strip()]
                media_item.tags.add(*tag_list)
            
            # 更新 Music
            music = form.save()
            
            messages.success(request, '音乐更新成功！')
            return redirect('music:detail', pk=music.pk)
    else:
        form = MusicForm(instance=music, user=request.user)
    
    return render(request, 'music/form.html', {'form': form, 'title': '编辑音乐'})


@login_required
def music_delete(request, pk):
    """删除音乐"""
    music = get_object_or_404(Music, pk=pk, media_item__user=request.user)
    
    if request.method == 'POST':
        # 删除关联的 MediaItem（会级联删除 Music）
        music.media_item.delete()
        messages.success(request, '音乐删除成功！')
        return redirect('music:list')
    
    return render(request, 'music/confirm_delete.html', {'music': music})
