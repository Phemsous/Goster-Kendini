from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q  

from .forms import JobForm
from .services import create_job_service
from .selectors import get_active_jobs


@login_required
def create_job(request):
    if str(request.user.role).lower() != 'producer':
        messages.error(request, "İş ilanı oluşturmak için 'Yapımcı / Casting' hesabı kullanmalısınız.")
        return redirect('job_list') 

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
    
    query = request.GET.get('q')    

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        ).distinct()
    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'query': query
    })