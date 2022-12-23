from django.db import models


class BaseAttendanceRateStatistics(models.Model):
    '''
    This model is mainly used for creating permission about statistics.
    It is not associated with any database table and does not contains any concrete data.
    '''

    class Meta:
        # No database table creation or deletion
        # operations will be performed for this model.
        managed = False

        # disable "add", "change", "delete"
        # and "view" default permissions
        default_permissions = ()


class StudentAttendanceRateStatistics(BaseAttendanceRateStatistics):
    class Meta(BaseAttendanceRateStatistics.Meta):
        permissions = (
            ('read_studentattendancerate',
             'allow read attendance rate of any student'),
        )


class TeacherAttendanceRateStatistics(BaseAttendanceRateStatistics):
    class Meta(BaseAttendanceRateStatistics.Meta):
        permissions = (
            ('read_teacherattendancerate',
             'allow read attendance rate of any teacher'),
        )
