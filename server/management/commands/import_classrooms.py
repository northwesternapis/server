import csv
from django.core.management.base import BaseCommand, CommandError
from server.models import *

class Command(BaseCommand):
    args = 'CLASSROOMS.csv - the file you want to parse. Should have six columns - the original (CAESAR) complete name, new building name, new room name, latitude, longitude, and NU maps link'
    help = 'Scrapes the Course Data web services for updated info'

    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError('Need a csv file with classroom data')

        with open(args[0], 'r') as file:
            classroom_file = csv.reader(file)
            next(classroom_file) # skip header row
            for row in classroom_file:
                building, new_building = Building.objects.get_or_create(
                    name=row[1],
                    defaults={'lat': row[3] if row[3] else None,
                              'lon': row[4] if row[4] else None,
                              'nu_maps_link': row[5] if row[5] else None})
                room, new_room = Room.objects.get_or_create(name=row[2],
                                                building=building)
                StringRoomMapping.objects.get_or_create(orig_string=row[0],
                                                        room=room)
                if new_building:
                    print 'created', building
                if new_room:
                    print 'created', room
