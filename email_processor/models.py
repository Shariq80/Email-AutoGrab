from django.db import models
from job_postings.models import JobPosting  # Update this import to the correct app

class Application(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=255)
    applicant_email = models.EmailField()
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/')
    received_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    analysis = models.TextField(blank=True, null=True)  # New field for storing Gemini API response

    def __str__(self):
        return f"{self.applicant_name} - {self.job_posting}"