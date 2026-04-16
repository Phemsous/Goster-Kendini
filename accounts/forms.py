from django import forms
from .models import User, Profile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Şifre'
        }),
        label='Şifre'
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Şifreyi Tekrar Girin'
        }),
        label='Şifre (Tekrar)'
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
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kullanıcı adınızı girin'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-posta adresinizi girin'
            }),
            'role': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Şifreler eşleşmiyor.')

        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'avatar_url', 'bio', 'skills_and_instruments', 'past_experience']
        labels = {
            'full_name': 'Ad Soyad',
            'avatar_url': 'Avatar URL',
            'bio': 'Biyografi',
            'skills_and_instruments': 'Yetenekler / Enstrümanlar',
            'past_experience': 'Geçmiş Deneyim',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar_url': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'skills_and_instruments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'past_experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }