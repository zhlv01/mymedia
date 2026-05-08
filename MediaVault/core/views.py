from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Category, MediaItem
from .forms import CategoryForm


def home(request):
    """首页"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    # 展示公开的内容及其分享码
    from share.models import Share
    public_shares = Share.objects.filter(
        media_item__is_public=True
    ).select_related('media_item').order_by('-created_at')[:12]
    
    return render(request, 'core/home.html', {'public_shares': public_shares})


@login_required
def dashboard(request):
    """仪表盘"""
    user = request.user
    
    # 统计数据
    music_count = MediaItem.objects.filter(user=user, media_type='music').count()
    video_count = MediaItem.objects.filter(user=user, media_type='video').count()
    note_count = MediaItem.objects.filter(user=user, media_type='note').count()
    
    # 最近添加
    recent_items = MediaItem.objects.filter(user=user).order_by('-created_at')[:10]
    
    context = {
        'music_count': music_count,
        'video_count': video_count,
        'note_count': note_count,
        'recent_items': recent_items,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def search(request):
    """搜索"""
    query = request.GET.get('q', '')
    media_type = request.GET.get('type', '')
    
    items = MediaItem.objects.filter(user=request.user)
    
    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    if media_type:
        items = items.filter(media_type=media_type)
    
    context = {
        'items': items,
        'query': query,
        'media_type': media_type,
    }
    return render(request, 'core/search.html', context)


@login_required
def category_list(request):
    """分类列表"""
    categories = Category.objects.filter(user=request.user)
    return render(request, 'core/category_list.html', {'categories': categories})


@login_required
def category_add(request):
    """添加分类"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('core:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'core/category_form.html', {'form': form, 'title': '添加分类'})


@login_required
def category_edit(request, pk):
    """编辑分类"""
    category = get_object_or_404(Category, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('core:category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'core/category_form.html', {'form': form, 'title': '编辑分类'})


@login_required
def category_delete(request, pk):
    """删除分类"""
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('core:category_list')
    
    return render(request, 'core/category_confirm_delete.html', {'category': category})
