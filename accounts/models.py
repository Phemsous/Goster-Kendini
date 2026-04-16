from django.db import models
from django.contrib.auth.models import AbstractUser


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

    def _str_(self):
        return f"{self.username} - {self.get_role_display()}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    avatar_url = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True)
    skills_and_instruments = models.TextField(blank=True)
    past_experience = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.full_name