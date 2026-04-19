from django.db import models
from accounts.models import User

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    video_url = models.TextField()
    category = models.CharField(max_length=100)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # --- YENİ EKLENEN FAVORİLER SATIRI ---
    favorites = models.ManyToManyField(User, related_name='favorite_videos', blank=True)

    # (Minik düzeltme: Çift alt çizgi eklendi)
    def __str__(self):
        return self.title


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class VideoReaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)