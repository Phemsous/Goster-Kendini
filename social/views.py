from django.shortcuts import render

def social_home(request):
    return render(request, 'social/social_home.html')