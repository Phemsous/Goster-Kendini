from django import forms
from .models import User, Job, TalentListing

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Şifre'}), 
        label="Şifre"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Şifreyi Doğrula'}), 
        label="Şifre (Tekrar)"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role']
        labels = {
            'username': 'Kullanıcı Adı',
            'email': 'E-posta Adresi',
            'role': 'Hesap Türü',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kullanıcı Adı'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-posta Adresi'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Şifreler eşleşmiyor, lütfen kontrol edin.")

        return cleaned_data


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
                'placeholder': 'Proje detaylarını, çekim tarihlerini ve aradığınız özellikleri buraya yazın...'
            }),
        }

# --- SİSTEMİ BOZMADAN EKLENEN YENİ FORM ---
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
            'category': forms.Select(attrs={'class': 'form-select'}),
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