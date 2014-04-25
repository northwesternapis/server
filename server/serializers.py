from django.contrib.auth.models import User, Group
from rest_framework import serializers
from server.models import *



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'term', 'school', 'instructor', 'subject', 'catalog_num', 'section', 'room', 'meeting_days', 'start_time', 'end_time', 'start_date', 'end_date', 'seats', 'overview', 'topic', 'attributes', 'requirements', 'component', 'class_num', 'course_id')

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('symbol', 'name', 'school', 'term')

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ('name', 'bio', 'address', 'phone', 'subjects', 'office_hours')

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ('term_id', 'name', 'start_date', 'end_date')
