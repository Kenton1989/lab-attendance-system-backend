
# class AbstractAttendance(models.Model):
#     session = models.ForeignKey(Session, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     check_in_state = models.CharField(max_length=20, blank=True)
#     check_in_datetime = models.DateTimeField(blank=True)

#     last_modify = models.DateTimeField(default=timezone.now)

#     remark = models.CharField(max_length=200, blank=True)

#     is_active = models.BooleanField(default=True)
from rest_framework import serializers
from rest_api.models import StudentAttendance, TeacherAttendance

COMMON_FIELDS = ['id', 'session', 'user',
                 'check_in_state', 'check_in_datetime',
                 'last_modify', 'remark', 'is_active']


class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = COMMON_FIELDS

class TeacherAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAttendance
        fields = COMMON_FIELDS