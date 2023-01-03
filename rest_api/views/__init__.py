from .user import UserViewSet
from .week import WeekViewSet
from .course import CourseViewSet
from .lab import LabViewSet
from .group import GroupViewSet
from .group_student import GroupStudentViewSet
from .session import SessionViewSet
from .student_make_up_session import StudentMakeUpSessionViewSet
from .attendance import StudentAttendanceViewSet, TeacherAttendanceViewSet
from .statistics import StudentAttendanceCountsViewSet, TeacherAttendanceCountsViewSet
from .user_attendance import UserStudentAttendanceViewSet, UserTeacherAttendanceViewSet
from .user_managed_data import UserManagedCourseViewSet, UserManagedGroupViewSet, UserManagedLabViewSet
from .user_role import UserRoleViewSet
