# email_processor/admin.py
from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant_name', 'applicant_email', 'job_posting', 'received_at', 'match_score')
    list_filter = ('job_posting', 'received_at')
    search_fields = ('applicant_name', 'applicant_email', 'job_posting__title')
    readonly_fields = ('received_at',)
    fieldsets = (
        (None, {
            'fields': ('job_posting', 'applicant_name', 'applicant_email', 'resume', 'match_score')
        }),
        ('Timestamp', {
            'fields': ('received_at',),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('job_posting', 'applicant_name', 'applicant_email', 'resume')
        return self.readonly_fields