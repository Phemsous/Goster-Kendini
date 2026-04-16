from .models import TalentListing


def get_active_talents():
    return TalentListing.objects.filter(is_active=True).order_by('-created_at')