from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import RegisterForm, JobForm, TalentListingForm
from .services import create_user_service, create_job_service, create_talent_ad_service
from .selectors import get_active_jobs, get_active_talents, get_latest_videos

def home(request):
    videos = get_latest_videos(limit=6)
    return render(request, 'home.html', {'videos': videos})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = create_user_service(**form.cleaned_data)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def create_job(request):
    # KAPIDAN ÇEVİRME: Sayfaya girişi en baştan engeller
    if str(request.user.role).lower() != 'producer':
        messages.error(request, "İş ilanı sayfasına girmek için 'Yapımcı / Casting' olmalısınız.")
        return redirect('home')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            try:
                create_job_service(request.user, **form.cleaned_data)
                messages.success(request, "İş ilanınız başarıyla yayınlandı!")
                return redirect('job_list')
            except ValueError as e:
                messages.error(request, str(e))
                return redirect('create_job')
    else:
        form = JobForm()
    return render(request, 'create_job.html', {'form': form})

def job_list(request):
    query = request.GET.get('q')
    jobs = get_active_jobs(query=query)
    return render(request, 'job_list.html', {'jobs': jobs, 'query': query})

@login_required
def create_talent_ad(request):
    # KAPIDAN ÇEVİRME: Sayfaya girişi en baştan engeller
    if str(request.user.role).lower() != 'artist':
        messages.error(request, "Yetenek ilanı sayfasına girmek için 'Sanatçı / Oyuncu' olmalısınız.")
        return redirect('home')

    if request.method == 'POST':
        form = TalentListingForm(request.POST)
        if form.is_valid():
            try:
                create_talent_ad_service(request.user, **form.cleaned_data)
                messages.success(request, "Yetenek profiliniz başarıyla yayınlandı!")
                return redirect('talent_list')
            except ValueError as e:
                messages.error(request, str(e))
                return redirect('create_talent_ad')
    else:
        form = TalentListingForm()
    return render(request, 'create_talent_ad.html', {'form': form})

def talent_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    talents = get_active_talents(query=query, category=category)
    return render(request, 'talent_list.html', {'talents': talents, 'query': query})