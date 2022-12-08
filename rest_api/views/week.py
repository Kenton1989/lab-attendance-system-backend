from rest_framework import viewsets, permissions
from rest_api.serializers import WeekSerializer
from rest_api.models import Week


class WeekViewSet(viewsets.ModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
