from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),

    # Ana sayfa
    path('', home, name='home'),

    # App URL'leri
    path('accounts/', include('accounts.urls')),
    path('videos/', include('videos.urls')),
    path('jobs/', include('jobs.urls')),
    path('talents/', include('talents.urls')),
    path('social/', include('social.urls')),
]