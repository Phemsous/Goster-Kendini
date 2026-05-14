from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Video

def get_all_videos():
    return Video.objects.all().order_by('-created_at')

def get_latest_videos(limit=12): 
    return Video.objects.all().order_by('-created_at')[:limit]

def get_video_by_id(video_id):
    return get_object_or_404(Video, id=video_id)

def get_filtered_videos(query=None, category=None, sort='new'):
    videos = Video.objects.all()
    if query:
        videos = videos.filter(
            Q(title__icontains=query) | Q(user__username__icontains=query)
        )
    if category:
        videos = videos.filter(category=category)
    if sort == 'popular':
        videos = videos.order_by('-like_count', '-created_at')
    else:
        videos = videos.order_by('-created_at')
    return videos