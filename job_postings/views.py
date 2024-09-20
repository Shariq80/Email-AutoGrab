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

class JobPostingListView(ListView):
    model = JobPosting
    template_name = 'job_postings/list.html'
    context_object_name = 'job_postings'

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

@require_POST
def generate_subject_line(request):
    data = json.loads(request.body)
    title = data.get('title')
    department = data.get('department')
    
    if not title or not department:
        return JsonResponse({'error': 'Title and department are required'}, status=400)
    
    subject_line = slugify(f"{title}-{department}-{uuid.uuid4().hex[:8]}")
    
    return JsonResponse({'subject_line': subject_line})