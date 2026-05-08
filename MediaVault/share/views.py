from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import markdown
from .models import Share
from core.models import MediaItem


def share_view(request, code):
    """分享链接访问"""
    share = get_object_or_404(Share, share_code=code)
    
    # 检查是否过期
    if share.expire_at and share.expire_at < timezone.now():
        messages.error(request, '该分享链接已过期')
        return redirect('core:home')
    
    # 检查密码
    if share.password:
        if request.method == 'POST':
            input_password = request.POST.get('password', '')
            if input_password != share.password:
                messages.error(request, '密码错误')
                return render(request, 'share/password.html')
            # 密码验证通过，设置session
            request.session[f'share_auth_{code}'] = True
        else:
            if not request.session.get(f'share_auth_{code}'):
                return render(request, 'share/password.html')
    
    # 增加访问次数
    share.increment_view()
    share.media_item.increment_view()
    
    # 根据媒体类型渲染
    media_type = share.media_item.media_type
    
    if media_type == 'music':
        music = share.media_item.music
        return render(request, 'share/music_view.html', {'share': share, 'music': music})
    elif media_type == 'video':
        video = share.media_item.video
        return render(request, 'share/video_view.html', {'share': share, 'video': video})
    elif media_type == 'note':
        note = share.media_item.note
        html_content = markdown.markdown(note.content, extensions=['extra', 'codehilite', 'toc'])
        return render(request, 'share/note_view.html', {'share': share, 'note': note, 'html_content': html_content})
    
    return render(request, 'share/view.html', {'share': share})


@login_required
def share_create(request, media_id):
    """创建分享链接"""
    media_item = get_object_or_404(MediaItem, pk=media_id, user=request.user)
    
    if request.method == 'POST':
        password = request.POST.get('password', '')
        expire_days = request.POST.get('expire_days', '')
        
        expire_at = None
        if expire_days:
            expire_at = timezone.now() + timezone.timedelta(days=int(expire_days))
        
        share = Share.objects.create(
            media_item=media_item,
            password=password,
            expire_at=expire_at,
            created_by=request.user
        )
        
        messages.success(request, f'分享链接创建成功！分享码：{share.share_code}')
        return redirect('share:my_shares')
    
    return render(request, 'share/create.html', {'media_item': media_item})


@login_required
def share_delete(request, pk):
    """删除分享链接"""
    share = get_object_or_404(Share, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        share.delete()
        messages.success(request, '分享链接已删除')
        return redirect('share:my_shares')
    
    return render(request, 'share/confirm_delete.html', {'share': share})


@login_required
def my_shares(request):
    """我的分享列表"""
    shares = Share.objects.filter(created_by=request.user).select_related('media_item', 'created_by')
    return render(request, 'share/list.html', {'shares': shares})


@login_required
def quick_public_share(request, media_id):
    """一键公开分享"""
    from django.http import JsonResponse

    media_item = get_object_or_404(MediaItem, pk=media_id, user=request.user)

    # 1. 设置为公开
    media_item.is_public = True
    media_item.save(update_fields=['is_public'])

    # 2. 创建或获取分享链接（永久有效，无密码）
    share, created = Share.objects.get_or_create(
        media_item=media_item,
        defaults={
            'created_by': request.user,
            'password': '',
            'expire_at': None
        }
    )

    # 返回JSON响应
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'share_code': share.share_code,
            'share_url': share.get_share_url(),
            'created': created
        })

    # 非AJAX请求，重定向到分享列表
    messages.success(request, f'已开启公开分享！分享码：{share.share_code}')
    return redirect('share:my_shares')


@login_required
def toggle_public_share(request, media_id):
    """切换公开分享状态"""
    from django.http import JsonResponse

    media_item = get_object_or_404(MediaItem, pk=media_id, user=request.user)

    # 切换公开状态
    media_item.is_public = not media_item.is_public
    media_item.save(update_fields=['is_public'])

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'is_public': media_item.is_public
        })

    return redirect(media_item.get_absolute_url())
