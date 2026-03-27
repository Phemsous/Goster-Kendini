from django.contrib import admin
from django.urls import path
# accounts.views içinden yeni eklediğimiz yetenek fonksiyonlarını da çağırıyoruz
from accounts.views import (
    home, register, user_login, user_logout, 
    create_job, job_list, 
    create_talent_ad, talent_list # Yeni eklenenler
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    
    # --- İŞ İLANI YOLLARI (Yapımcı Arıyor) ---
    path('jobs/', job_list, name='job_list'), 
    path('jobs/new/', create_job, name='create_job'),
    
    # --- YETENEK İLANI YOLLARI (Sanatçı Arıyor) ---
    path('talents/', talent_list, name='talent_list'),       # Yeteneklerin listelendiği sayfa
    path('talents/new/', create_talent_ad, name='create_talent_ad'), # Sanatçının ilan verme sayfası
]