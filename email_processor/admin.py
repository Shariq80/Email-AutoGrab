# email_processor/admin.py
from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant_name', 'applicant_email', 'job_posting', 'received_at', 'processed')
    list_filter = ('job_posting', 'processed')
    search_fields = ('applicant_name', 'applicant_email')
    readonly_fields = ('received_at',)

    fieldsets = (
        (None, {
            'fields': ('job_posting', 'applicant_name', 'applicant_email', 'resume', 'cover_letter')
        }),
        ('Processing Information', {
            'fields': ('received_at', 'processed', 'analysis')
        }),
    )