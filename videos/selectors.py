from django.shortcuts import get_object_or_404
from .models import Video

def get_all_videos():
    return Video.objects.all().order_by('-created_at')

def get_latest_videos(limit=12): 
    return Video.objects.all().order_by('-created_at')[:limit]

def get_video_by_id(video_id):
    return get_object_or_404(Video, id=video_id)