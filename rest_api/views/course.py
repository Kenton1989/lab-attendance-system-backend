from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_api.serializers import CourseSerializer
from rest_api.models import Course, User
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


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    filter_backends = (filters.DjangoFilterBackend, SearchFilter,)
    search_fields = ('code', 'title',)
    filterset_class = CourseFilterSet
