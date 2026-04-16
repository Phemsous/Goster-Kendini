from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import JobForm
from .services import create_job_service
from .selectors import get_active_jobs


@login_required
def create_job(request):
    if str(request.user.role).lower() != 'producer':
        messages.error(request, "İş ilanı oluşturmak için 'Yapımcı / Casting' hesabı kullanmalısınız.")
        return redirect('home')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            create_job_service(
                producer=request.user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description']
            )
            messages.success(request, 'İş ilanı başarıyla oluşturuldu.')
            return redirect('job_list')
    else:
        form = JobForm()

    return render(request, 'jobs/create_job.html', {'form': form})


def job_list(request):
    jobs = get_active_jobs()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

# Create your views here.
