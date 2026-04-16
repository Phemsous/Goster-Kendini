from .models import Video


def get_all_videos():
    return Video.objects.all().order_by('-created_at')


def get_latest_videos(limit=6):
    return Video.objects.all().order_by('-created_at')[:limit]


def get_video_by_id(video_id):
    return Video.objects.get(id=video_id)