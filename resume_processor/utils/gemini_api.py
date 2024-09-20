# resume_processor/utils/gemini_api.py

import os
import google.generativeai as genai
from django.conf import settings
from job_postings.models import JobPosting
from email_processor.models import Application

# Configure the Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

def analyze_resume(resume_text, job_description):
    """
    Analyze a resume against a job description using the Gemini API.
    Returns a match score between 0 and 1.
    """
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Analyze the following resume for the job description provided. 
    Provide a match score between 0 and 1, where 1 is a perfect match.
    Only return the numeric score, without any additional text or explanation.
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_description}
    
    Match Score:
    """
    
    response = model.generate_content(prompt)
    
    try:
        match_score = float(response.text.strip())
        return max(0, min(match_score, 1))  # Ensure score is between 0 and 1
    except ValueError:
        print(f"Error parsing match score: {response.text}")
        return 0  # Default to 0 if parsing fails

def extract_text_from_resume(file_path):
    """
    Extract text from a resume file (PDF or DOCX).
    """
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension.lower() == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.
    """
    try:
        import PyPDF2
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except ImportError:
        print("PyPDF2 is not installed. Please install it using: pip install PyPDF2")
        return ""

def extract_text_from_docx(file_path):
    """
    Extract text from a DOCX file.
    """
    try:
        import docx
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except ImportError:
        print("python-docx is not installed. Please install it using: pip install python-docx")
        return ""

def process_resumes():
    """
    Process all unprocessed resumes and update match scores.
    """
    applications = Application.objects.filter(match_score__isnull=True)
    
    for application in applications:
        resume_path = os.path.join(settings.MEDIA_ROOT, application.resume.name)
        resume_text = extract_text_from_resume(resume_path)
        job_description = application.job_posting.description
        
        match_score = analyze_resume(resume_text, job_description)
        
        application.match_score = match_score
        application.save()
        
        print(f"Processed resume for {application.applicant_name}. Match score: {match_score}")

if __name__ == '__main__':
    process_resumes()