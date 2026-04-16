from .models import TalentListing


def create_talent_ad_service(artist, title, category, experience, skills):
    return TalentListing.objects.create(
        artist=artist,
        title=title,
        category=category,
        experience=experience,
        skills=skills
    )