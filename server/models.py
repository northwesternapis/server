from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    quarter = models.CharField(max_length=6)
    professor = models.CharField(max_length=40)
    school = models.CharField(max_length=4) # character code
    subject = models.CharField(max_length=20)
    sequence = models.CharField(max_length=5)
    class_number = models.IntegerField()

    def __unicode__(self):
        return '%s %d: %s %s' % (self.year, self.quarter, \
                                 self.title, self.sequence)
