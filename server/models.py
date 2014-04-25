from django.db import models

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
    name = models.CharField(max_length=60)
    term = models.ForeignKey('Term')

class Subject(models.Model):
    symbol = models.CharField(max_length=8)
    name = models.CharField(max_length=50)
    school = models.ForeignKey('School')
    term = models.ForeignKey('Term')

class Instructor(models.Model):
    name = models.CharField(max_length=60)
    bio = models.TextField(null=True)
    address = models.TextField(null=True)
    phone = models.CharField(max_length=20, null=True)
    subjects = models.ManyToManyField('Subject')
    office_hours = models.TextField(null=True)

class Course(models.Model):
    title = models.CharField(max_length=100)
    term = models.ForeignKey('Term')
    school = models.CharField(max_length=10) # use code instead of foreignkey
    instructor = models.ForeignKey('Instructor')

    subject = models.CharField(max_length=20) # use code instead of ForeignKey
    catalog_num = models.CharField(max_length=10)
    section = models.CharField(max_length=6)

    room = models.CharField(max_length=50)
    meeting_days = models.CharField(max_length=11, null=True)
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

class CourseDesc(models.Model):
    course = models.ForeignKey('Course')
    name = models.CharField(max_length=40)
    desc = models.TextField()

# Labs, discussions, etc.
class CourseComponent(models.Model):
    component = models.CharField(max_length=10)
    meeting_days = models.CharField(max_length=11, null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    section = models.CharField(max_length=6)
    room = models.CharField(max_length=50)
    course = models.ForeignKey('Course')

