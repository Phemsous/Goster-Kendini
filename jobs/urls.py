from django.urls import path
from .views import create_job, job_list

urlpatterns = [
    path('create/', create_job, name='create_job'),
    path('', job_list, name='job_list'),
]