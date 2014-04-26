from django.contrib.auth.models import User, Group
from rest_framework import serializers
from server.models import *



class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ('term_id', 'name', 'start_date', 'end_date')

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('symbol', 'name')

class SubjectSerializer(serializers.ModelSerializer):
    school = serializers.SlugRelatedField(read_only=True, slug_field='symbol')
    class Meta:
        model = Subject
        fields = ('symbol', 'name')

class InstructorSerializer(serializers.ModelSerializer):
    subjects = serializers.SlugRelatedField(many=True, read_only=True, slug_field='symbol')
    class Meta:
        model = Instructor
        fields = ('name', 'bio', 'address', 'phone', 'subjects', 'office_hours')

class InstructorCourseSerializer(serializers.ModelSerializer):
    subjects = serializers.SlugRelatedField(many=True, read_only=True, slug_field='symbol')
    class Meta:
        model = Instructor
        fields = ('name', 'bio', 'address', 'phone', 'office_hours')

class CourseDescSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDesc
        fields = ('name', 'desc')

class CourseComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseComponent
        fields = ('component', 'meeting_days', 'start_time', 'end_time', 'section', 'room')

class CourseSerializer(serializers.ModelSerializer):
    term = serializers.SlugRelatedField(read_only=True, slug_field='name')
    instructor = InstructorCourseSerializer()
    coursedesc_set = CourseDescSerializer()
    coursecomponent_set = CourseComponentSerializer()
    class Meta:
        model = Course
        fields = ('title', 'term', 'school', 'instructor', 'subject', 'catalog_num', 'section', 'room', 'meeting_days', 'start_time', 'end_time', 'start_date', 'end_date', 'seats', 'overview', 'topic', 'attributes', 'requirements', 'component', 'class_num', 'course_id', 'coursedesc_set', 'coursecomponent_set')

