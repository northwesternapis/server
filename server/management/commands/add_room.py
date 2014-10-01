from django.core.management.base import BaseCommand, CommandError
from server.models import *

class Command(BaseCommand):
    args = 'Original classroom string, building name, room name'
    help = 'Add a classroom to the database'

    def handle(self, *args, **options):
        if len(args) < 3:
            print 'Missing arguments'
            return

        orig_string = args[0]
        building_name = args[1]
        room_name = args[2]

        building, _ = Building.objects.get_or_create(name=building_name)
        room, room_created = Room.objects.get_or_create(
            building=building,
            name=room_name,
            defaults={'full_name': '%s %s' % (building_name, room_name)})
        StringRoomMapping.objects.get_or_create(
            room=room, orig_string=orig_string)

        print room.id
