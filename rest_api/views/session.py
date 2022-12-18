from rest_framework.viewsets import ModelViewSet
from rest_api.serializers import SessionSerializer, StudentMakeUpSessionSerializer
from rest_api.models import Session, StudentMakeUpSession


class SessionViewSet(ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class StudentMakeUpSessionViewSet(ModelViewSet):
    queryset = StudentMakeUpSession.objects.all()
    serializer_class = StudentMakeUpSessionSerializer
