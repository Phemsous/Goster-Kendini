from django import forms
from .models import TalentListing


class TalentListingForm(forms.ModelForm):
    class Meta:
        model = TalentListing
        fields = ['title', 'category', 'experience', 'skills']
        labels = {
            'title': 'Yetenek Başlığı',
            'category': 'Kategori',
            'experience': 'Deneyimler',
            'skills': 'Ek Yetenekler / Uzmanlıklar',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Örn: Profesyonel Oyuncu ve Seslendirme Sanatçısı'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'experience': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Daha önce yer aldığınız projeler, aldığınız eğitimler...'
            }),
            'skills': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Örn: İngilizce, Ehliyet, Binicilik, Piyano...'
            }),
        }