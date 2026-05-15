from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .forms import TalentListingForm
from .services import create_talent_ad_service
from .selectors import get_active_talents


@login_required
def create_talent_ad(request):
    if str(request.user.role).lower() != 'artist':
        messages.error(request, "Yetenek ilanı oluşturmak için 'Sanatçı / Oyuncu' hesabı kullanmalısınız.")
        return redirect('home')

    if request.method == 'POST':
        form = TalentListingForm(request.POST)
        if form.is_valid():
            create_talent_ad_service(
                artist=request.user,
                title=form.cleaned_data['title'],
                category=form.cleaned_data['category'],
                experience=form.cleaned_data['experience'],
                skills=form.cleaned_data['skills']
            )
            messages.success(request, 'Yetenek ilanı başarıyla oluşturuldu.')
            return redirect('talent_list')
    else:
        form = TalentListingForm()

    return render(request, 'talents/create_talent_ad.html', {'form': form})


def talent_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    talents = get_active_talents()

    if query:
        talents = talents.filter(
            Q(title__icontains=query) |
            Q(experience__icontains=query) |
            Q(skills__icontains=query) |
            Q(artist__username__icontains=query)
        )

    if category:
        talents = talents.filter(category=category)

    return render(request, 'talents/talent_list.html', {
        'talents': talents,
        'query': query,
        'category': category,
    })