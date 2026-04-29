# email_processor/utils/gmail_api.py

import os
import base64
import django
import email
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from django.conf import settings
from job_postings.models import JobPosting
from email_processor.models import Application



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def fetch_emails(service, query):
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        process_email(service, msg)

def process_email(service, msg):
    payload = msg['payload']
    headers = payload['headers']
    
    # Extract subject and sender
    subject = next(header['value'] for header in headers if header['name'].lower() == 'subject')
    sender = next(header['value'] for header in headers if header['name'].lower() == 'from')
    
    # Find matching job posting
    try:
        job_posting = JobPosting.objects.get(subject_line__iexact=subject)
    except JobPosting.DoesNotExist:
        print(f"No matching job posting found for subject: {subject}")
        return
    
    # Extract applicant name and email from sender
    applicant_name, applicant_email = parse_sender(sender)
    
    # Process attachments
    attachments = []
    if 'parts' in payload:
        attachments = [part for part in payload['parts'] if part['filename']]
    
    for attachment in attachments:
        if attachment['filename'].lower().endswith(('.pdf', '.docx')):
            attachment_id = attachment['body']['attachmentId']
            attachment_content = service.users().messages().attachments().get(
                userId='me', messageId=msg['id'], id=attachment_id
            ).execute()
            
            file_data = base64.urlsafe_b64decode(attachment_content['data'].encode('UTF-8'))
            
            # Save resume
            resume_path = save_resume(file_data, attachment['filename'])
            
            # Create Application object
            Application.objects.create(
                job_posting=job_posting,
                applicant_name=applicant_name,
                applicant_email=applicant_email,
                resume=resume_path
            )
            
            print(f"Processed application for {applicant_name} ({applicant_email}) for job: {job_posting.title}")
            break  # Assume only one resume per email

def parse_sender(sender):
    # Basic parsing, you might need to improve this based on your email formats
    parts = sender.split('<')
    if len(parts) == 2:
        name = parts[0].strip()
        email = parts[1].strip('>')
    else:
        name = ''
        email = sender
    return name, email

def save_resume(file_data, filename):
    # Ensure the resumes directory exists
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'resumes'), exist_ok=True)
    
    # Generate a unique filename
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(os.path.join(settings.MEDIA_ROOT, 'resumes', filename)):
        filename = f"{base}_{counter}{ext}"
        counter += 1
    
    file_path = os.path.join(settings.MEDIA_ROOT, 'resumes', filename)
    
    with open(file_path, 'wb') as f:
        f.write(file_data)
    
    return os.path.join('resumes', filename)

def fetch_and_process_emails():
    service = get_gmail_service()
    
    # Fetch emails for all job postings
    job_postings = JobPosting.objects.all()
    for job_posting in job_postings:
        query = f"subject:{job_posting.subject_line}"
        fetch_emails(service, query)

if __name__ == '__main__':
    fetch_and_process_emails()