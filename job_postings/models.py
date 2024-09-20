from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid

class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    description = models.TextField()
    subject_line = models.CharField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.subject_line:
            # Generate unique subject line
            self.subject_line = slugify(f"{self.title}-{self.department}-{uuid.uuid4().hex[:8]}")
        super(JobPosting, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} - {self.job_posting.title}"


# class JobPosting(models.Model):
#     title = models.CharField(max_length=200)
#     department = models.CharField(max_length=100)
#     job_type = models.CharField(max_length=50)
#     location = models.CharField(max_length=100)
#     description = models.TextField()
#     subject_line = models.CharField(max_length=200, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title