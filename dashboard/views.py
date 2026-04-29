# dashboard/views.py
from django.shortcuts import render
from job_postings.models import JobPosting
from email_processor.models import Application

def dashboard(request):
    context = {
        'recent_job_postings': JobPosting.objects.order_by('-created_at')[:5],
        'recent_applications': Application.objects.order_by('-received_at')[:5],
    }
    return render(request, 'dashboard/index.html', context)