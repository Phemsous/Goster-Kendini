from django.db import models
from accounts.models import User


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
    title = models.CharField(max_length=255)
    experience = models.TextField()
    skills = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.artist.username} - {self.title}"

# Create your models here.
