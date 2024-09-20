# job_postings/forms.py
from django import forms
from .models import JobPosting

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'department', 'job_type', 'location', 'description', 'subject_line']