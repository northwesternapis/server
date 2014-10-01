from django.core.management.base import BaseCommand, CommandError
from server.models import APIProject

class Command(BaseCommand):
    args = ''
    help = 'Reset request counts for all active projects'

    def handle(self, *args, **options):
        for project in APIProject.objects.filter(is_active=True).iterator():
            project.requests_sent = 0
            project.save()
