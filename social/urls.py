from django.urls import path
from .views import social_home

urlpatterns = [
    path('', social_home, name='social_home'),
]