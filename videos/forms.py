from django import forms
from .models import Video, Comment


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_url', 'category']
        labels = {
            'title': 'Video Başlığı',
            'video_url': 'Video URL',
            'category': 'Kategori',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Video başlığını girin'
            }),
            'video_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Video bağlantısını girin'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kategori girin'
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Yorum',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Yorumunuzu yazın'
            }),
        }