from rest_framework.viewsets import ModelViewSet
from rest_api.serializers import StudentMakeUpSessionSerializer
from rest_api.models import StudentMakeUpSession, Group
from django_filters import rest_framework as filters


class StudentMakeUpSessionFilterSet(filters.FilterSet):
    original_group = filters.ModelChoiceFilter(
        field_name='original_session__group',
        queryset=Group.objects.all(),
    )
    make_up_group = filters.ModelChoiceFilter(
        field_name='make_up_session__group',
        queryset=Group.objects.all(),
    )

    class Meta:
        model = StudentMakeUpSession
        fields = ('user', 'original_session', 'make_up_session')


class StudentMakeUpSessionViewSet(ModelViewSet):
    queryset = StudentMakeUpSession.objects.all()
    serializer_class = StudentMakeUpSessionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StudentMakeUpSessionFilterSet
