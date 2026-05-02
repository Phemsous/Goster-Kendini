from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:user_id>/', views.conversation, name='conversation'),
    path('unread/', views.unread_count, name='unread_count'),
]