from rest_framework.viewsets import ModelViewSet
from rest_api.serializers import GroupStudentSerializer
from rest_api.models import GroupStudent
from django_filters import rest_framework as filters


class GroupStudentViewSet(ModelViewSet):
    queryset = GroupStudent.objects.all()
    serializer_class = GroupStudentSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('student', 'group',)

    class Meta:
        model = GroupStudent
