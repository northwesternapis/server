from django.db.models import Building, Room

# Table that maps all existing room names to room objects

def get_room_by_string(room_name):
    # All room names have the same format:
    # the building name comes first, then the room name.

    # Usually, the first one, two, or three words are the building name;
    # keep guessing until we find something. Of course, there are
    # so we have to handle all of those too.

    room_parts = room_name.split()

    # Buildings with different names e.g. Tech Institute
    # and Technological Institute be the same object
    if room_parts[0] == 'Tech':
        room_parts[0] = 'Technological'

    # If not a special case, should be in the normal format BUILDING ROOM
    # First, try one word
    try:
        building = Building.objects.get(name=room_parts[0])
    except Building.DoesNotExist:
        pass

    # Two words
    try:
        building = Building.objects.get(name=' '.join(room_parts[:2]))
    except Building.DoesNotExist:
        pass

    # Three words
    try:
        building = Building.objects.get(name=' '.join(room_parts[:3]))
    except Building.DoesNotExist:
        pass

    # Four words
    try:
        building = Building.objects.get(name=' '.join(room_parts[:4]))
    except Building.DoesNotExist:
        pass

    # Fail and be loud about it
