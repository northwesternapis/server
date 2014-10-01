import datetime
from django.core.management.base import BaseCommand, CommandError
from server.models import APIProject

class Command(BaseCommand):
    args = ''
    help = 'Check for projects that have expired and make them inactive'

    def handle(self, *args, **options):
        expired_projects = APIProject.objects.filter(
            is_active=True,
            expiration_date__lt=datetime.datetime.now())
        print 'Found %d expired projects' % expired_projects.count()
        for project in expired_projects.iterator():
            project.is_active = False
            project.save()
