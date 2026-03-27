from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Özelleştirilmiş Kullanıcı Modeli (AYNEN KORUNDU)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('artist', 'Sanatçı / Oyuncu'),
        ('producer', 'Yapımcı / Casting'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='artist')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

# 2. Profil Bilgileri (AYNEN KORUNDU)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    avatar_url = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True)
    skills_and_instruments = models.TextField(blank=True)
    past_experience = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

# 3. Videolar (AYNEN KORUNDU)
class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    video_url = models.TextField()
    category = models.CharField(max_length=100)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

# 4. İş İlanları (AYNEN KORUNDU - related_name 'job_posts' olarak tutuldu)
class Job(models.Model):
    producer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_posts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

# --- YENİ EKLEME: 5. YETENEK İLANLARI (Sanatçılar için) ---
class TalentListing(models.Model):
    CATEGORY_CHOICES = (
        ('actor', 'Oyuncu'),
        ('musician', 'Müzisyen'),
        ('dancer', 'Dansçı'),
        ('model', 'Model'),
        ('other', 'Diğer'),
    )
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='talent_ads')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=255, help_text="Örn: Profesyonel Tiyatro Oyuncusu")
    experience = models.TextField(help_text="Daha önce yer aldığınız projeler")
    skills = models.CharField(max_length=500, help_text="Örn: Eskrim, Ehliyet, Akıcı İngilizce")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artist.username} - {self.title}"

# 6. Yorumlar (AYNEN KORUNDU)
class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 7. Mesajlaşma Sistemi (AYNEN KORUNDU)
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# 8. Takip Sistemi (AYNEN KORUNDU)
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

# 9. Video Reaksiyonları (AYNEN KORUNDU)
class VideoReaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10) # 'like' veya 'dislike'
    created_at = models.DateTimeField(auto_now_add=True)