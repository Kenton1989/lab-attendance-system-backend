from rest_api.models import Group, GroupStudent
from rest_framework import serializers
from .user import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'course', 'name', 'is_active']


class GroupStudentSerializer(serializers.ModelSerializer):
    student = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Group
        fields = ['student', 'group', 'seat']
