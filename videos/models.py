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
    favorites = models.ManyToManyField(User, related_name='favorite_videos', blank=True)

    def __str__(self):
        return self.title

    @property
    def get_embed_url(self):
        """
        Normal YouTube linklerini (watch?v=...) iframe içinde 
        çalışacak 'embed' formatına dönüştürür.
        """
        url = self.video_url
        if not url:
            return ""

        if 'watch?v=' in url:
            video_id = url.split('v=')[1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        
        elif 'youtu.be/' in url:
            video_id = url.split('/')[-1].split('?')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        
        return url


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