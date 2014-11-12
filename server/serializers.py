from django.contrib.auth.models import User, Group
from rest_framework import serializers
from server.models import *



class TermSerializer(serializers.ModelSerializer):
    id = serializers.Field(source='term_id')

    class Meta:
        model = Term
        fields = ('id', 'name', 'start_date', 'end_date')

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('symbol', 'name')

class SubjectSerializer(serializers.ModelSerializer):
    school = serializers.SlugRelatedField(read_only=True, slug_field='symbol')

    class Meta:
        model = Subject
        fields = ('symbol', 'name')

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
    start_time = serializers.TimeField(source='start_time', format='%H:%M')
    end_time = serializers.TimeField(source='end_time', format='%H:%M')

    class Meta:
        model = CourseComponent
        fields = ('component', 'meeting_days', 'start_time', 'end_time', 'section', 'room')


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('id', 'name', 'lat', 'lon', 'nu_maps_link')

class RoomSerializer(serializers.ModelSerializer):
    building_id = serializers.SlugRelatedField(source='building', read_only=True, slug_field='id')

    class Meta:
        model = Room
        fields = ('id', 'building_id', 'name')

class RoomDetailsSerializer(serializers.ModelSerializer):
    building = BuildingSerializer()

    class Meta:
        model = Room
        fields = ('id', 'building', 'name')

class CourseRoomSerializer(serializers.ModelSerializer):
    building_id = serializers.SlugRelatedField(source='building', read_only=True, slug_field='id')
    building_name = serializers.SlugRelatedField(source='building', read_only=True, slug_field='name')

    class Meta:
        model = Room
        fields = ('id', 'building_id', 'building_name', 'name')


class CourseSerializer(serializers.ModelSerializer):
    term = serializers.SlugRelatedField(read_only=True, slug_field='name')
    instructor = InstructorCourseSerializer()
    course_descriptions = CourseDescSerializer()
    course_components = CourseComponentSerializer()
    start_time = serializers.TimeField(source='start_time', format='%H:%M')
    end_time = serializers.TimeField(source='end_time', format='%H:%M')
    room = CourseRoomSerializer()

    class Meta:
        model = Course
        fields = ('id', 'title', 'term', 'school', 'instructor', 'subject', 'catalog_num', 'section', 'room', 'meeting_days', 'start_time', 'end_time', 'start_date', 'end_date', 'seats', 'overview', 'topic', 'attributes', 'requirements', 'component', 'class_num', 'course_id', 'course_descriptions', 'course_components')


class CourseSummarySerializer(serializers.ModelSerializer):
    term = serializers.SlugRelatedField(read_only=True, slug_field='name')
    instructor = serializers.SlugRelatedField(read_only=True, slug_field='name')
    start_time = serializers.TimeField(source='start_time', format='%H:%M')
    end_time = serializers.TimeField(source='end_time', format='%H:%M')
    room = serializers.SlugRelatedField(source='room', read_only=True, slug_field='full_name')

    class Meta:
        model = Course
        fields = ('id', 'title', 'term', 'instructor', 'subject', 'catalog_num', 'section', 'room', 'meeting_days', 'start_time', 'end_time', 'seats', 'topic', 'component', 'class_num', 'course_id')

