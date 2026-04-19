from django.shortcuts import render

def home(request):
    return render(request, 'videos/video_list.html')