# resume_processor/management/commands/process_resumes.py

from django.core.management.base import BaseCommand
from resume_processor.utils.resume_processor import process_all_resumes

class Command(BaseCommand):
    help = 'Process all unprocessed resumes'

    def handle(self, *args, **options):
        self.stdout.write("Processing all unprocessed resumes...")
        process_all_resumes()
        self.stdout.write(self.style.SUCCESS("Resume processing completed successfully"))