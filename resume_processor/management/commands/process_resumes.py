# resume_processor/management/commands/process_resumes.py

from django.core.management.base import BaseCommand, CommandError
from resume_processor.utils.resume_processor import (
    process_all_resumes,
    process_resumes_for_job_posting,
    get_top_candidates,
    update_resume_scores
)

class Command(BaseCommand):
    help = 'Process resumes and calculate match scores using Gemini API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--job-posting-id',
            type=int,
            help='Process resumes for a specific job posting'
        )
        parser.add_argument(
            '--top-candidates',
            type=int,
            help='Get top N candidates for a specific job posting'
        )
        parser.add_argument(
            '--update-scores',
            action='store_true',
            help='Update scores for all processed resumes'
        )

    def handle(self, *args, **options):
        if options['job_posting_id'] and options['top_candidates']:
            self.stdout.write(self.style.SUCCESS(f"Getting top {options['top_candidates']} candidates for job posting {options['job_posting_id']}..."))
            get_top_candidates(options['job_posting_id'], options['top_candidates'])
        elif options['job_posting_id']:
            self.stdout.write(self.style.SUCCESS(f"Processing resumes for job posting {options['job_posting_id']}..."))
            process_resumes_for_job_posting(options['job_posting_id'])
        elif options['update_scores']:
            self.stdout.write(self.style.SUCCESS("Updating scores for all processed resumes..."))
            update_resume_scores()
        else:
            self.stdout.write(self.style.SUCCESS("Processing all unprocessed resumes..."))
            process_all_resumes()
        
        self.stdout.write(self.style.SUCCESS('Resume processing completed successfully'))