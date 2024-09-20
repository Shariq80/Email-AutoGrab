from django.core.management.base import BaseCommand
from email_processor.utils.gmail_api import fetch_and_process_emails
from email_processor.utils.email_processor import process_emails

class Command(BaseCommand):
    help = 'Fetch and process emails for job applications'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to fetch and process emails...'))
        process_emails()
        self.stdout.write(self.style.SUCCESS('Successfully fetched and processed emails'))