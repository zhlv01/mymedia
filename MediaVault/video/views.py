from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Video
from .forms import VideoForm
from core.models import MediaItem


@login_required
def video_list(request):
    """视频列表"""
    video_items = Video.objects.filter(media_item__user=request.user).select_related('media_item')
    
    tag = request.GET.get('tag')
    if tag:
        video_items = video_items.filter(media_item__tags__name=tag)
    
    category = request.GET.get('category')
    if category:
        video_items = video_items.filter(media_item__category__id=category)
    
    context = {
        'video_items': video_items,
        'tag_filter': tag,
        'category_filter': category,
    }
    return render(request, 'video/list.html', context)


@login_required
def video_detail(request, pk):
    """视频详情"""
    video = get_object_or_404(Video, pk=pk, media_item__user=request.user)
    video.media_item.increment_view()
    return render(request, 'video/detail.html', {'video': video})


@login_required
def video_add(request):
    """添加视频"""
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            media_item = MediaItem.objects.create(
                user=request.user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                cover_image=form.cleaned_data.get('cover_image'),
                category=form.cleaned_data.get('category'),
                media_type='video',
                is_public=form.cleaned_data.get('is_public', False)
            )
            
            tags_str = form.cleaned_data.get('tags', '')
            if tags_str:
                tag_list = [t.strip() for t in tags_str.split(',') if t.strip()]
                media_item.tags.add(*tag_list)
            
            video = form.save(commit=False)
            video.media_item = media_item
            video.save()
            
            messages.success(request, '视频添加成功！')
            return redirect('video:detail', pk=video.pk)
    else:
        form = VideoForm(user=request.user)
    
    return render(request, 'video/form.html', {'form': form, 'title': '添加视频'})


@login_required
def video_edit(request, pk):
    """编辑视频"""
    video = get_object_or_404(Video, pk=pk, media_item__user=request.user)
    
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video, user=request.user)
        if form.is_valid():
            media_item = video.media_item
            media_item.title = form.cleaned_data['title']
            media_item.description = form.cleaned_data['description']
            if form.cleaned_data.get('cover_image'):
                media_item.cover_image = form.cleaned_data['cover_image']
            media_item.category = form.cleaned_data.get('category')
            media_item.is_public = form.cleaned_data.get('is_public', False)
            media_item.save()
            
            tags_str = form.cleaned_data.get('tags', '')
            media_item.tags.clear()
            if tags_str:
                tag_list = [t.strip() for t in tags_str.split(',') if t.strip()]
                media_item.tags.add(*tag_list)
            
            form.save()
            messages.success(request, '视频更新成功！')
            return redirect('video:detail', pk=video.pk)
    else:
        form = VideoForm(instance=video, user=request.user)
    
    return render(request, 'video/form.html', {'form': form, 'title': '编辑视频'})


@login_required
def video_delete(request, pk):
    """删除视频"""
    video = get_object_or_404(Video, pk=pk, media_item__user=request.user)
    
    if request.method == 'POST':
        video.media_item.delete()
        messages.success(request, '视频删除成功！')
        return redirect('video:list')
    
    return render(request, 'video/confirm_delete.html', {'video': video})
