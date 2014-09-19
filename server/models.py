from django.db import models
from django.contrib.auth.models import User

# the list of subjects - could be a list of tuples, but 
# we rely on the SOAP service and it could change,
# so it'll probably have to be a table
class Term(models.Model):
    term_id = models.PositiveIntegerField()
    name = models.CharField(max_length=20)
    shopping_cart_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return self.name

class School(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=80)
    term = models.ForeignKey('Term')

    def __unicode__(self):
        return self.name

class Subject(models.Model):
    symbol = models.CharField(max_length=8)
    name = models.CharField(max_length=50)
    school = models.ForeignKey('School')
    term = models.ForeignKey('Term')

    def __unicode__(self):
        return self.symbol

class Instructor(models.Model):
    name = models.CharField(max_length=60)
    bio = models.TextField(null=True)
    address = models.TextField(null=True)
    phone = models.CharField(max_length=50, null=True)
    subjects = models.ManyToManyField('Subject')
    office_hours = models.TextField(null=True)

class Course(models.Model):
    title = models.CharField(max_length=100)
    term = models.ForeignKey('Term')
    school = models.CharField(max_length=10) # use code instead of foreignkey
    instructor = models.ForeignKey('Instructor')

    subject = models.CharField(max_length=50) # use code instead of ForeignKey
    catalog_num = models.CharField(max_length=10)
    section = models.CharField(max_length=6)

    room = models.ForeignKey('Room', null=True)
    meeting_days = models.CharField(max_length=20, null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    seats = models.PositiveSmallIntegerField(null=True)
    overview = models.TextField(null=True)
    topic = models.TextField(null=True)

    attributes = models.TextField(null=True)
    requirements = models.TextField(null=True)
    component = models.CharField(max_length=10) # Lecture, lab, etc.

    # housekeeping
    class_num = models.PositiveIntegerField(null=True)
    course_id = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return '%s: %s %s (%s)' % (self.term, \
                 self.catalog_num, self.title, self.section)

class Building(models.Model):
    name = models.TextField()
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    nu_maps_link = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.name

class Room(models.Model):
    building = models.ForeignKey('Building')
    name = models.TextField()
    full_name = models.TextField()

    def __unicode__(self):
        return self.full_name


class StringRoomMapping(models.Model):
    orig_string = models.TextField()
    room = models.ForeignKey('Room')

    def __unicode__(self):
        return '%s -> %s' % (self.orig_string, self.room)


# Optional bits that can describe prerequisites, textbooks, etc
class CourseDesc(models.Model):
    course = models.ForeignKey('Course', related_name='course_descriptions')
    name = models.CharField(max_length=40)
    desc = models.TextField()

# Labs, discussions, etc.
class CourseComponent(models.Model):
    course = models.ForeignKey('Course', related_name='course_components')
    component = models.CharField(max_length=10)
    meeting_days = models.CharField(max_length=20, null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    section = models.CharField(max_length=6)
    room = models.CharField(max_length=50, null=True)

class ScrapeRecord(models.Model):
    date = models.DateTimeField(auto_now=True)
    term = models.ForeignKey('Term')
    school = models.ForeignKey('School')
    subject = models.ForeignKey('Subject')

    def __unicode__(self):
        return '%s, %s' % (self.date, self.subject)


request_statuses = (
    ('A', 'Approved'),
    ('S', 'Submitted'),
    ('R', 'Rejected'),
)
class APIProjectRequest(models.Model):
    owner = models.ForeignKey(User)
    name = models.TextField()
    description = models.TextField()
    how_long = models.TextField()

    status = models.CharField(max_length=1, choices=request_statuses, default='S')
    date_submitted = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return '%s: %s\'s request for %s' % (self.date_submitted, self.owner.get_full_name(), self.name)

class APIProject(models.Model):
    owner = models.ForeignKey(User, related_name='api_projects')
    name = models.TextField()

    api_key = models.CharField(max_length=16)
    requests_sent = models.IntegerField(default=0)
    daily_limit = models.IntegerField(default=10000)

    original_request = models.ForeignKey('APIProjectRequest')
    approved_by = models.ForeignKey(User, related_name='projects_approved')
    date_approved = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.name)

class AllowedReferrer(models.Model):
    APIProject = models.ForeignKey('APIProject')
    url = models.TextField()
