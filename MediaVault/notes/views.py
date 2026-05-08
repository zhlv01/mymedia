from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import markdown
from .models import Note
from .forms import NoteForm
from core.models import MediaItem


@login_required
def note_list(request):
    """笔记列表"""
    note_items = Note.objects.filter(media_item__user=request.user).select_related('media_item')
    
    tag = request.GET.get('tag')
    if tag:
        note_items = note_items.filter(media_item__tags__name=tag)
    
    category = request.GET.get('category')
    if category:
        note_items = note_items.filter(media_item__category__id=category)
    
    context = {
        'note_items': note_items,
        'tag_filter': tag,
        'category_filter': category,
    }
    return render(request, 'notes/list.html', context)


@login_required
def note_detail(request, pk):
    """笔记详情"""
    note = get_object_or_404(Note, pk=pk, media_item__user=request.user)
    note.media_item.increment_view()
    
    html_content = markdown.markdown(
        note.content,
        extensions=['extra', 'codehilite', 'toc']
    )
    
    context = {
        'note': note,
        'html_content': html_content,
    }
    return render(request, 'notes/detail.html', context)


@login_required
def note_add(request):
    """添加笔记"""
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            media_item = MediaItem.objects.create(
                user=request.user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                cover_image=form.cleaned_data.get('cover_image'),
                category=form.cleaned_data.get('category'),
                media_type='note',
                is_public=form.cleaned_data.get('is_public', False)
            )
            
            tags_str = form.cleaned_data.get('tags', '')
            if tags_str:
                tag_list = [t.strip() for t in tags_str.split(',') if t.strip()]
                media_item.tags.add(*tag_list)
            
            note = form.save(commit=False)
            note.media_item = media_item
            note.save()
            
            messages.success(request, '笔记创建成功！')
            return redirect('notes:detail', pk=note.pk)
    else:
        form = NoteForm(user=request.user)
    
    return render(request, 'notes/form.html', {'form': form, 'title': '新建笔记'})


@login_required
def note_edit(request, pk):
    """编辑笔记"""
    note = get_object_or_404(Note, pk=pk, media_item__user=request.user)
    
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note, user=request.user)
        if form.is_valid():
            media_item = note.media_item
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
            messages.success(request, '笔记更新成功！')
            return redirect('notes:detail', pk=note.pk)
    else:
        form = NoteForm(instance=note, user=request.user)
    
    return render(request, 'notes/form.html', {'form': form, 'title': '编辑笔记'})


@login_required
def note_delete(request, pk):
    """删除笔记"""
    note = get_object_or_404(Note, pk=pk, media_item__user=request.user)
    
    if request.method == 'POST':
        note.media_item.delete()
        messages.success(request, '笔记删除成功！')
        return redirect('notes:list')
    
    return render(request, 'notes/confirm_delete.html', {'note': note})
