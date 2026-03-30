from .models import Video, Job, TalentListing
from django.db.models import Q

def get_latest_videos(limit=6):
    """Ana sayfa için son videoları getirir."""
    return Video.objects.all().order_by('-created_at')[:limit]

def get_active_jobs(query=None):
    """İş ilanlarını listeler ve arama yapar."""
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return jobs

def get_active_talents(query=None, category=None):
    """Yetenek ilanlarını listeler, arama ve kategori filtresi uygular."""
    talents = TalentListing.objects.filter(is_active=True).order_by('-created_at')
    if query:
        talents = talents.filter(
            Q(title__icontains=query) | Q(skills__icontains=query) | Q(experience__icontains=query)
        )
    if category:
        talents = talents.filter(category=category)
    return talents