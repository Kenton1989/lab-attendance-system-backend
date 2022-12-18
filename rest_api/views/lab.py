from rest_framework.viewsets import ModelViewSet
from rest_api.serializers import LabSerializer
from rest_api.models import Lab


class LabViewSet(ModelViewSet):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer
