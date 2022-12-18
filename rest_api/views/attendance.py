from rest_framework.viewsets import ModelViewSet
from rest_api.serializers import StudentAttendanceSerializer, TeacherAttendanceSerializer
from rest_api.models import StudentAttendance, TeacherAttendance


class StudentAttendanceViewSet(ModelViewSet):
    queryset = StudentAttendance.objects.all()
    serializer_class = StudentAttendanceSerializer


class TeacherAttendanceViewSet(ModelViewSet):
    queryset = TeacherAttendance.objects.all()
    serializer_class = TeacherAttendanceSerializer
