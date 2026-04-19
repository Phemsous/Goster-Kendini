from django.contrib import admin
from django.urls import path, include
from videos.views import video_list 

urlpatterns = [
    path('admin/', admin.site.urls),   
    path('', video_list, name='home'),

    path('accounts/', include('accounts.urls')),
    path('videos/', include('videos.urls')),
    path('jobs/', include('jobs.urls')),
    path('talents/', include('talents.urls')),
    path('social/', include('social.urls')),
]