from django.urls import path
from .views import register, user_login, user_logout, profile_detail, profile_edit

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile_detail, name='profile_detail'),
    path('profile/edit/', profile_edit, name='profile_edit'),
]