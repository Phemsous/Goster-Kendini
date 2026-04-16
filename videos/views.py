from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Video
from .forms import VideoForm, CommentForm
from .services import create_video_service, create_comment_service, react_to_video_service
from .selectors import get_all_videos, get_video_by_id


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


def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    comment_form = CommentForm()

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
        'comment_form': comment_form
    })


@login_required
def react_video(request, video_id, reaction_type):
    video = get_object_or_404(Video, id=video_id)

    if reaction_type not in ['like', 'dislike']:
        messages.error(request, 'Geçersiz reaksiyon.')
        return redirect('video_detail', video_id=video.id)

    react_to_video_service(request.user, video, reaction_type)
    messages.success(request, 'Reaksiyon kaydedildi.')
    return redirect('video_detail', video_id=video.id)