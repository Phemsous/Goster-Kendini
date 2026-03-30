from .models import User, Job, TalentListing

def create_user_service(username, password, role='artist', **extra_fields):
    """Kullanıcı kaydı ve şifreleme."""
    extra_fields.pop('confirm_password', None)
    user = User(username=username, role=role, **extra_fields)
    user.set_password(password)
    user.save()
    return user

def create_job_service(producer, title, description):
    """İş ilanı kaydı. Servis düzeyinde rol doğrulaması yapar."""
    if str(producer.role).lower() != 'producer':
        raise ValueError("İş ilanı yayınlamak için 'Yapımcı' olmalısınız.")
    return Job.objects.create(producer=producer, title=title, description=description)

def create_talent_ad_service(artist, category, title, experience, skills):
    """Yetenek ilanı kaydı. Servis düzeyinde rol doğrulaması yapar."""
    if str(artist.role).lower() != 'artist':
        raise ValueError("Yetenek ilanı yayınlamak için 'Sanatçı' olmalısınız.")
    return TalentListing.objects.create(
        artist=artist, category=category, title=title, experience=experience, skills=skills
    )