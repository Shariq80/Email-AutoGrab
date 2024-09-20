# job_postings/admin.py
from django.contrib import admin
from .models import JobPosting

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'job_type', 'location', 'created_at', 'updated_at')
    list_filter = ('department', 'job_type', 'location')
    search_fields = ('title', 'description', 'subject_line')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'department', 'job_type', 'location', 'description', 'subject_line')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )