from django.contrib.auth.models import User, Group
from rest_framework import serializers
from server.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

#class CourseSerializer(serializers.Serializer):
#    pk = serializer
class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'year', 'quarter', 'professor', 'school', 'subject', 'sequence', 'class_number')

