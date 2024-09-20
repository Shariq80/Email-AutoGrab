# resume_processor/utils/resume_processor.py

import os
from django.conf import settings
from job_postings.models import JobPosting
from email_processor.models import Application
from .gemini_api import analyze_resume, extract_text_from_resume

def process_all_resumes():
    """
    Process all unprocessed resumes for all job postings.
    """
    unprocessed_applications = Application.objects.filter(match_score__isnull=True)
  
    for application in unprocessed_applications:
        process_single_resume(application)

def process_single_resume(application):
    """
    Process a single resume for a given application.
    """
    try:
        resume_path = os.path.join(settings.MEDIA_ROOT, application.resume.name)
        resume_text = extract_text_from_resume(resume_path)
        job_description = application.job_posting.description
        
        match_score = analyze_resume(resume_text, job_description)
        
        application.match_score = match_score
        application.save()
        
        print(f"Processed resume for {application.applicant_name}. Match score: {match_score}")
    except Exception as e:
        print(f"Error processing resume for {application.applicant_name}: {str(e)}")

def process_resumes_for_job_posting(job_posting_id):
    """
    Process all unprocessed resumes for a specific job posting.
    """
    try:
        job_posting = JobPosting.objects.get(id=job_posting_id)
        unprocessed_applications = Application.objects.filter(
            job_posting=job_posting,
            match_score__isnull=True
        )
        
        for application in unprocessed_applications:
            process_single_resume(application)
        
        print(f"Processed all resumes for job posting: {job_posting.title}")
    except JobPosting.DoesNotExist:
        print(f"Job posting with ID {job_posting_id} does not exist.")

def get_top_candidates(job_posting_id, top_n=5):
    """
    Get the top N candidates for a specific job posting based on match score.
    """
    try:
        job_posting = JobPosting.objects.get(id=job_posting_id)
        top_candidates = Application.objects.filter(
            job_posting=job_posting,
            match_score__isnull=False
        ).order_by('-match_score')[:top_n]
        
        print(f"Top {top_n} candidates for {job_posting.title}:")
        for candidate in top_candidates:
            print(f"- {candidate.applicant_name}: {candidate.match_score}")
        
        return top_candidates
    except JobPosting.DoesNotExist:
        print(f"Job posting with ID {job_posting_id} does not exist.")
        return []

def update_resume_scores():
    """
    Update scores for all processed resumes.
    """
    processed_applications = Application.objects.filter(match_score__isnull=False)
    
    for application in processed_applications:
        process_single_resume(application)
    
    print(f"Updated scores for {processed_applications.count()} applications.")

if __name__ == '__main__':
    process_all_resumes()