# job_postings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import JobPosting
from .forms import JobPostingForm

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