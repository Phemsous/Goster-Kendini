from django.urls import path
from .views import create_talent_ad, talent_list

urlpatterns = [
    path('create/', create_talent_ad, name='create_talent_ad'),
    path('', talent_list, name='talent_list'),
]