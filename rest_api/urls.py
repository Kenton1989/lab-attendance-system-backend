from django.urls import path, include
from rest_api import views
from rest_api.views import token
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter
from dynamic_preferences.api.viewsets import GlobalPreferencesViewSet

rest_router = SimpleRouter()
rest_router.register(r'weeks', views.WeekViewSet)
rest_router.register(r'users', views.UserViewSet)
users_router = NestedSimpleRouter(rest_router, r'users', lookup='user')
rest_router.register(r'labs', views.LabViewSet)
rest_router.register(r'courses', views.CourseViewSet)
rest_router.register(r'groups', views.GroupViewSet)
rest_router.register(r'group_students', views.GroupStudentViewSet)
rest_router.register(r'sessions', views.SessionViewSet)
rest_router.register(r'student_make_up_sessions',
                     views.StudentMakeUpSessionViewSet)
rest_router.register(r'student_attendances', views.StudentAttendanceViewSet)
rest_router.register(r'teacher_attendances', views.TeacherAttendanceViewSet)
rest_router.register(r'statistics/student_attendances',
                     views.StudentAttendanceCountsViewSet,
                     basename='statistics-student-attendance')
rest_router.register(r'statistics/teacher_attendances',
                     views.TeacherAttendanceCountsViewSet,
                     basename='statistics-teacher-attendance')
rest_router.register(r'preferences/',
                     GlobalPreferencesViewSet,
                     basename='global-preference')

urlpatterns = [
    # authentication API
    path('users/me/tokens/', token.CreateToken.as_view()),
    path('users/me/tokens/current/', token.RevokeToken.as_view()),
    path('users/me/tokens/all/', token.RevokeAllToken.as_view()),

    path('', include(rest_router.urls)),
]
