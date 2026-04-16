from django.urls import path
from .views import upload_video, video_list, video_detail, react_video

urlpatterns = [
    path('upload/', upload_video, name='upload_video'),
    path('', video_list, name='video_list'),
    path('<int:video_id>/', video_detail, name='video_detail'),
    path('<int:video_id>/react/<str:reaction_type>/', react_video, name='react_video'),
]