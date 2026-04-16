from .models import Job


def get_active_jobs():
    return Job.objects.filter(is_active=True).order_by('-created_at')