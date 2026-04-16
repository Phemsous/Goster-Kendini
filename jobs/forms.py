from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description']
        labels = {
            'title': 'İlan Başlığı',
            'description': 'İlan Detayları',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Örn: Kısa Film İçin Başrol Kadın Oyuncu Aranıyor'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Proje detaylarını, çekim tarihlerini ve aradığınız özellikleri yazın'
            }),
        }