from rest_framework.filters import SearchFilter
from .base import BaseModelViewSet
from rest_api.serializers import CourseSerializer
from rest_api.models import Course, User
from rest_api.permissions import CourseAccessPermission
from django_filters import rest_framework as filters


class CourseFilterSet(filters.FilterSet):
    coordinators_contain = filters.ModelChoiceFilter(
        field_name="coordinators",
        queryset=User.objects.all(),
    )
    students_contain = filters.ModelChoiceFilter(
        field_name="groups__students",
        queryset=User.objects.all(),
    )

    class Meta:
        model = Course
        fields = ('is_active',)


class CourseViewSet(BaseModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    filter_backends = (filters.DjangoFilterBackend, SearchFilter,)
    search_fields = ('code', 'title',)
    filterset_class = CourseFilterSet

    permission_classes = (CourseAccessPermission, )
