from rest_framework.schemas.openapi import AutoSchema


class BaseSchema(AutoSchema):
    pass


class RoleSchema(BaseSchema):
    def __init__(self):
        super().__init__(operation_id_base='Role')


class UserRoleSchema(BaseSchema):
    def __init__(self):
        super().__init__(operation_id_base='UserRole')


class UserManagedCourseSchema(BaseSchema):
    def __init__(self):
        super().__init__(operation_id_base='UserManagedCourse')


class UserManagedGroupSchema(BaseSchema):
    def __init__(self):
        super().__init__(operation_id_base='UserManagedGroup')


class UserManagedLabSchema(BaseSchema):
    def __init__(self):
        super().__init__(operation_id_base='UserManagedLab')


class UserStudentAttendanceSchema(BaseSchema):
    def __init__(self):
        super().__init__(operation_id_base='UserStudentAttendance')


class UserTeacherAttendanceSchema(BaseSchema):
    def __init__(self):
        super().__init__(operation_id_base='UserTeacherAttendance')


class UserStudentAttendanceCourseOptionSchema(BaseSchema):
    def __init__(self):
        super().__init__(operation_id_base='UserStudentAttendanceCourseOption')


class UserTeacherAttendanceCourseOptionSchema(BaseSchema):
    def __init__(self):
        super().__init__(operation_id_base='UserTeacherAttendanceCourseOption')


class StudentAttendanceStatisticsSchema(BaseSchema):
    def __init__(self):
        super().__init__(operation_id_base='StudentAttendanceStatistics')


class TeacherAttendanceStatisticsSchema(BaseSchema):
    def __init__(self):
        super().__init__(operation_id_base='TeacherAttendanceStatistics')
