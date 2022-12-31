from rest_framework.filters import SearchFilter
from .base import BaseModelViewSet
from rest_api.serializers import GroupSerializer
from rest_api.models import Group, User
from rest_api.permissions import GroupAccessPermission
from django_filters import rest_framework as filters


class GroupFilterSet(filters.FilterSet):
    supervisors_contain = filters.ModelChoiceFilter(
        'supervisors',
        queryset=User.objects.all(),
    )
    teachers_contain = filters.ModelChoiceFilter(
        'teachers',
        queryset=User.objects.all(),
    )
    students_contain = filters.ModelChoiceFilter(
        'students',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Group
        fields = ('course', 'lab', 'is_active',)


class GroupViewSet(BaseModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    filter_backends = (filters.DjangoFilterBackend, SearchFilter,)
    search_fields = ('name',)

    permission_classes = (GroupAccessPermission, )
