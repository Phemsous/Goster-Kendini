from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, ProfileForm
from .services import create_user_service
from .models import Profile, User


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = create_user_service(**form.cleaned_data)
            login(request, user)
            messages.success(request, 'Kayıt başarılı.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Giriş başarılı.')
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Çıkış yapıldı.')
    return redirect('home')


@login_required
def profile_detail(request):
    favorite_videos = request.user.favorite_videos.all()
    my_videos = request.user.videos.all().order_by('-created_at')
    return render(request, 'accounts/profile.html', {
        'favorite_videos': favorite_videos,
        'my_videos': my_videos,
    })


@login_required
def profile_edit(request):
    if request.method == 'POST':
        request.user.username = request.POST.get('username', request.user.username)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.role = request.POST.get('role', request.user.role)
        request.user.save()
        messages.success(request, 'Profil güncellendi.')
        return redirect('profile_detail')
    return render(request, 'accounts/profile_edit.html')


@login_required
def user_search(request):
    query = request.GET.get('q', '')
    role = request.GET.get('role', '')

    users = User.objects.exclude(id=request.user.id)

    if query:
        users = users.filter(username__icontains=query)

    if role in ('artist', 'producer'):
        users = users.filter(role=role)

    if not query and not role:
        users = User.objects.none()

    return render(request, 'accounts/user_search.html', {
        'users': users,
        'query': query,
        'selected_role': role,
    })


@login_required
def public_profile(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    videos = other_user.videos.all()
    return render(request, 'accounts/public_profile.html', {
        'other_user': other_user,
        'videos': videos
    })