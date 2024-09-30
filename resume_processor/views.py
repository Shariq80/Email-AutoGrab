from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from email_processor.models import Application

# Create your views here.

def application_detail(request, application_id):
    try:
        application = Application.objects.get(id=application_id)
    except ObjectDoesNotExist:
        raise Http404("Application not found")
    
    context = {
        'application': application,
    }
    return render(request, 'resume_processor/application_detail.html', context)
