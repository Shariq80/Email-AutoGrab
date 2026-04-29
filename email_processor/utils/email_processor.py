# email_processor/utils/email_processor.py

import os
import base64
from email import message_from_bytes
from email.utils import parseaddr
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from job_postings.models import JobPosting
from email_processor.models import Application
from .gmail_api import get_gmail_service

def process_emails():
    """
    Main function to process emails for all job postings.
    """
    service = get_gmail_service()
    job_postings = JobPosting.objects.all()

    for job_posting in job_postings:
        query = f"subject:{job_posting.subject_line}"
        process_emails_for_job_posting(service, job_posting, query)

def process_emails_for_job_posting(service, job_posting, query):
    """
    Process emails for a specific job posting.
    """
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
        email_data = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
        email_message = message_from_bytes(email_data)
        
        process_single_email(email_message, job_posting)

def process_single_email(email_message, job_posting):
    """
    Process a single email message.
    """
    subject = email_message['subject']
    from_address = email_message['from']
    applicant_name, applicant_email = parseaddr(from_address)

    # Process attachments
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        if filename and filename.lower().endswith(('.pdf', '.docx')):
            file_data = part.get_payload(decode=True)
            resume_path = save_resume(file_data, filename)

            # Create or update Application
            Application.objects.update_or_create(
                job_posting=job_posting,
                applicant_email=applicant_email,
                defaults={
                    'applicant_name': applicant_name,
                    'resume': resume_path
                }
            )

            print(f"Processed application for {applicant_name} ({applicant_email}) for job: {job_posting.title}")
            break  # Assume only one resume per email

def save_resume(file_data, filename):
    """
    Save the resume file and return the file path.
    """
    # Generate a unique filename
    base, ext = os.path.splitext(filename)
    counter = 1
    while default_storage.exists(os.path.join('resumes', filename)):
        filename = f"{base}_{counter}{ext}"
        counter += 1
    
    file_path = os.path.join('resumes', filename)
    
    # Save the file using Django's storage system
    default_storage.save(file_path, ContentFile(file_data))
    
    return file_path

if __name__ == '__main__':
    process_emails()