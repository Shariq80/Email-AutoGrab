# job_postings/forms.py
from django import forms
from .models import JobPosting
from email_processor.models import Application

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'department', 'job_type', 'location', 'description', 'subject_line']
        widgets = {
            'subject_line': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject_line'].required = False
        
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['applicant_name', 'applicant_email', 'resume']
        widgets = {
            'applicant_name': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'applicant_email': forms.EmailInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'resume': forms.FileInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
        }