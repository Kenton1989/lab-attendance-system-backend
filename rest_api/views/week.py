from rest_framework.viewsets import ModelViewSet
from rest_api.serializers import WeekSerializer
from rest_api.models import Week


class WeekViewSet(ModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer
