from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import Video
from .forms import VideoForm, CommentForm
from .services import create_video_service, create_comment_service, react_to_video_service
from .selectors import get_all_videos, get_video_by_id, get_filtered_videos


@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            create_video_service(
                user=request.user,
                title=form.cleaned_data['title'],
                video_url=form.cleaned_data['video_url'],
                category=form.cleaned_data['category']
            )
            messages.success(request, 'Video başarıyla yüklendi.')
            return redirect('video_list')
    else:
        form = VideoForm()
    return render(request, 'videos/upload_video.html', {'form': form})


def video_list(request):
    videos = get_all_videos()
    return render(request, 'videos/video_list.html', {'videos': videos})


def video_explore(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    sort = request.GET.get('sort', 'new')
    videos = get_filtered_videos(query=query or None, category=category or None, sort=sort)
    categories = [
        ('müzik', 'Müzik & Enstrüman'),
        ('dans', 'Dans & Koreografi'),
        ('oyunculuk', 'Oyunculuk & Tiyatro'),
        ('komedi', 'Stand-up & Komedi'),
        ('diger', 'Diğer'),
    ]
    return render(request, 'videos/video_explore.html', {
        'videos': videos,
        'query': query,
        'category': category,
        'sort': sort,
        'categories': categories,
        'video_count': videos.count(),
    })


def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    comment_form = CommentForm()

    user_reaction = None
    if request.user.is_authenticated:
        from .models import VideoReaction
        reaction_obj = VideoReaction.objects.filter(user=request.user, video=video).first()
        user_reaction = reaction_obj.reaction_type if reaction_obj else None

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            create_comment_service(
                user=request.user,
                video=video,
                content=comment_form.cleaned_data['content']
            )
            messages.success(request, 'Yorum eklendi.')
            return redirect('video_detail', video_id=video.id)

    return render(request, 'videos/video_detail.html', {
        'video': video,
        'comment_form': comment_form,
        'user_reaction': user_reaction,
    })


@login_required
def react_video(request, video_id, reaction_type):
    video = get_object_or_404(Video, id=video_id)

    if reaction_type not in ['like', 'dislike']:
        return JsonResponse({'error': 'Geçersiz reaksiyon.'}, status=400)

    from .models import VideoReaction

    existing = VideoReaction.objects.filter(user=request.user, video=video).first()

    if existing:
        if existing.reaction_type == reaction_type:
            existing.delete()
            user_reaction = None
        else:
            existing.reaction_type = reaction_type
            existing.save()
            user_reaction = reaction_type
    else:
        VideoReaction.objects.create(user=request.user, video=video, reaction_type=reaction_type)
        user_reaction = reaction_type

    video.like_count = VideoReaction.objects.filter(video=video, reaction_type='like').count()
    video.dislike_count = VideoReaction.objects.filter(video=video, reaction_type='dislike').count()
    video.save()

    return JsonResponse({
        'like_count': video.like_count,
        'dislike_count': video.dislike_count,
        'user_reaction': user_reaction,
    })


@login_required(login_url='/accounts/login/')
def favorite_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if request.user in video.favorites.all():
        video.favorites.remove(request.user)
        is_favorited = False
    else:
        video.favorites.add(request.user)
        is_favorited = True

    return JsonResponse({'is_favorited': is_favorited})