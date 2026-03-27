from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, JobForm, TalentListingForm # TalentListingForm eklendi
from .models import Video, Job, TalentListing # TalentListing eklendi
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.contrib import messages

def home(request):
    videos = Video.objects.all().order_by('-created_at')[:6]
    return render(request, 'home.html', {'videos': videos})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
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

# --- GÜNCELLENMİŞ İŞ İLANI FONKSİYONU (AYNEN KORUNDU) ---

@login_required
def create_job(request):
    user_role = str(request.user.role).strip().lower()
    
    if user_role != 'producer':
        messages.error(request, f"Hata: Rolünüz '{user_role}' olarak görünüyor. İlan vermek için 'producer' olmalısınız.")
        return redirect('home')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.producer = request.user
            job.save()
            messages.success(request, "İlan başarıyla yayınlandı!")
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'create_job.html', {'form': form})

def job_list(request):
    query = request.GET.get('q')
    if query:
        jobs = Job.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            is_active=True
        ).order_by('-created_at')
    else:
        jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    
    return render(request, 'job_list.html', {'jobs': jobs, 'query': query})

# --- YENİ: SANATÇI YETENEK İLANI SİSTEMİ (HİÇBİR ŞEYİ BOZMADAN EKLENDİ) ---

@login_required
def create_talent_ad(request):
    # Sanatçı kontrolü (create_job ile aynı mantıkta)
    user_role = str(request.user.role).strip().lower()
    
    if user_role != 'artist':
        messages.error(request, f"Hata: Rolünüz '{user_role}'. Yetenek ilanı vermek için 'artist' olmalısınız.")
        return redirect('home')
    
    if request.method == 'POST':
        form = TalentListingForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.artist = request.user
            ad.save()
            messages.success(request, "Yetenek profiliniz başarıyla yayınlandı!")
            return redirect('talent_list')
    else:
        form = TalentListingForm()
    return render(request, 'create_talent_ad.html', {'form': form})

def talent_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    
    talents = TalentListing.objects.filter(is_active=True).order_by('-created_at')
    
    if query:
        talents = talents.filter(
            Q(title__icontains=query) | Q(skills__icontains=query) | Q(experience__icontains=query)
        )
    
    if category:
        talents = talents.filter(category=category)
        
    return render(request, 'talent_list.html', {'talents': talents, 'query': query})