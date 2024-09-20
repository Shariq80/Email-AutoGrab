# job_postings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from .models import JobPosting
from .forms import JobPostingForm
import json
import uuid

from django.shortcuts import get_object_or_404, redirect
from .forms import JobApplicationForm

class JobPostingListView(ListView):
    model = JobPosting
    template_name = 'job_postings/list.html'
    context_object_name = 'job_postings'

    def get_queryset(self):
        queryset = JobPosting.objects.all()
        search_query = self.request.GET.get('search')
        department = self.request.GET.get('department')
        job_type = self.request.GET.get('job_type')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        if department:
            queryset = queryset.filter(department=department)
        if job_type:
            queryset = queryset.filter(job_type=job_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = JobPosting.objects.values_list('department', flat=True).distinct()
        context['job_types'] = JobPosting.objects.values_list('job_type', flat=True).distinct()
        return context

class JobPostingCreateView(CreateView):
    model = JobPosting
    form_class = JobPostingForm
    template_name = 'job_postings/create.html'
    success_url = '/job-postings/'

class JobPostingUpdateView(UpdateView):
    model = JobPosting
    form_class = JobPostingForm
    template_name = 'job_postings/update.html'
    success_url = '/job-postings/'

class JobPostingDeleteView(DeleteView):
    model = JobPosting
    template_name = 'job_postings/delete.html'
    success_url = '/job-postings/'

class JobPostingDetailView(DetailView):
    model = JobPosting
    template_name = 'job_postings/detail.html'
    context_object_name = 'job_posting'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        applications = self.object.application_set.all().order_by('-match_score')
        context['applications'] = applications
        return context


@require_POST
def generate_subject_line(request):
    data = json.loads(request.body)
    title = data.get('title')
    department = data.get('department')
    
    if not title or not department:
        return JsonResponse({'error': 'Title and department are required'}, status=400)
    
    subject_line = slugify(f"{title}-{department}-{uuid.uuid4().hex[:8]}")
    
    return JsonResponse({'subject_line': subject_line})

def job_application(request, pk):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_posting = job_posting
            application.save()
            return redirect('job_posting_detail', pk=pk)
    else:
        form = JobApplicationForm()
    return render(request, 'job_postings/apply.html', {'form': form, 'job_posting': job_posting})