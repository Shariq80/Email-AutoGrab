from django.db import models
from job_postings.models import JobPosting

# Create your models here.
class Application(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=200)
    applicant_email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    received_at = models.DateTimeField(auto_now_add=True)
    match_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.applicant_name} - {self.job_posting.title}"