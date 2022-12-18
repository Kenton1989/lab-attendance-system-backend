from rest_framework.viewsets import ModelViewSet
from rest_api.serializers import GroupSerializer, GroupStudentSerializer
from rest_api.models import Group, GroupStudent


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupStudentViewSet(ModelViewSet):
    queryset = GroupStudent.objects.all()
    serializer_class = GroupStudentSerializer
