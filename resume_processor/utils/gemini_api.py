# resume_processor/utils/gemini_api.py

import json
import logging
import os
from google.cloud import aiplatform
from google.oauth2 import service_account
from django.conf import settings
import google.generativeai as genai
from email_processor.models import Application
from google.ai import generativelanguage as glm
import re
from google.ai.generativelanguage_v1beta.types import content

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

def analyze_resume(resume_text, job_description):
    """
    Analyze a resume against a job description using the Gemini API.
    Returns the raw response from Gemini.
    """
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    prompt = f"""
    Analyze the following resume against the job description. Provide a JSON response with the following structure:
    {{
      "key_skills": {{"matching": [], "missing": []}},
      "academic_qualification": "",
      "achievements": [],
      "responsibilities": {{"matching": [], "missing": []}},
      "years_of_experience": "",
      "industry": "",
      "location": "",
      "overall_rating": 0,
      "recommendation": ""
    }}
    Ensure 'overall_rating' is between 0 and 10.

    Resume:
    {resume_text}
    
    Job Description:
    {job_description}
    """
    
    response = model.generate_content(prompt)
    return response.text

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
    Process all unprocessed resumes and update with detailed analysis.
    """
    applications = Application.objects.filter(processed=False)
    
    for application in applications:
        process_application(application.id)
        
        print(f"Processed resume for {application.applicant_name}. Match score: {application.match_score}")

def process_application(application_id):
    try:
        application = Application.objects.get(id=application_id)
        
        if application.processed:
            logger.info(f"Application {application_id} already processed. Skipping.")
            return
        
        resume_path = os.path.join(settings.MEDIA_ROOT, application.resume.name)
        resume_text = extract_text_from_resume(resume_path)
        job_description = application.job_posting.description

        response_data = analyze_resume(resume_text, job_description)
        logger.info(f"Gemini API response for application {application_id}: {response_data}")

        process_gemini_response(application, response_data)

        application.processed = True
        application.save()
        logger.info(f"Successfully processed application {application_id}")
    except Exception as e:
        logger.error(f"Error processing application {application_id}: {str(e)}")

def process_gemini_response(application, raw_response):
    try:
        # Extract JSON from the response text
        json_match = re.search(r'```json\s*(.*?)\s*```', raw_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = raw_response

        # Store the raw response in the analysis field
        application.analysis = json_str
        application.processed = True
        application.save()
        logger.info(f"Successfully updated application {application.id} with Gemini response")
    except Exception as e:
        logger.error(f"Error processing Gemini response for application {application.id}: {str(e)}")

if __name__ == '__main__':
    process_resumes()