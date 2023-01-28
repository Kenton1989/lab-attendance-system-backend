from django.urls import path, include
from rest_api import views
from rest_api.views import token
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter
from dynamic_preferences.api.viewsets import GlobalPreferencesViewSet
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

rest_router = SimpleRouter(trailing_slash=False)
rest_router.register(r'weeks', views.WeekViewSet)
rest_router.register(r'roles', views.RoleViewSet)
rest_router.register(r'users', views.UserViewSet)
users_nested_router = NestedSimpleRouter(rest_router, r'users', lookup='user')
users_nested_router.register(
    r'roles', views.UserRoleViewSet, basename='user-roles')
users_nested_router.register(
    r'managed_courses', views.UserManagedCourseViewSet, basename='user-managed-courses')
users_nested_router.register(
    r'managed_groups', views.UserManagedGroupViewSet, basename='user-managed-groups')
users_nested_router.register(
    r'managed_labs', views.UserManagedLabViewSet, basename='user-managed-labs')
users_nested_router.register(
    r'student_attendances/course_options', views.UserStudentAttendanceViewSet.CourseOptionsViewSet, basename='user-student-attendances-course-options')
users_nested_router.register(
    r'teacher_attendances/course_options', views.UserTeacherAttendanceViewSet.CourseOptionsViewSet, basename='user-teacher-attendances-course-options')
users_nested_router.register(
    r'student_attendances', views.UserStudentAttendanceViewSet, basename='user-student-attendances')
users_nested_router.register(
    r'teacher_attendances', views.UserTeacherAttendanceViewSet, basename='user-teacher-attendances')
rest_router.register(r'labs', views.LabViewSet)
rest_router.register(r'courses', views.CourseViewSet)
rest_router.register(r'groups', views.GroupViewSet)
rest_router.register(r'group_students', views.GroupStudentViewSet)
rest_router.register(r'sessions', views.SessionViewSet)
rest_router.register(r'student_make_up_sessions',
                     views.StudentMakeUpSessionViewSet)
rest_router.register(r'student_attendances', views.StudentAttendanceViewSet)
rest_router.register(r'teacher_attendances', views.TeacherAttendanceViewSet)
rest_router.register(r'student_attendances/statistics', views.StudentAttendanceStatsViewSet,
                     basename='statistics-student-attendance')
rest_router.register(r'teacher_attendances/statistics', views.TeacherAttendanceStatsViewSet,
                     basename='statistics-teacher-attendance')
rest_router.register(r'preferences', GlobalPreferencesViewSet,
                     basename='preference')


urlpatterns = [
    # authentication API
    path('users/me/tokens', token.CreateToken.as_view()),
    path('users/me/tokens/current', token.RevokeToken.as_view()),
    path('users/me/tokens/all', token.RevokeAllToken.as_view()),

    path('openapi', get_schema_view(
        title="Lab Attendance System API",
        description="API for all things",
        version="1.0.0",
        authentication_classes=[],
        permission_classes=[],
    ), name='openapi-schema'),

    path('swagger-ui', TemplateView.as_view(
        template_name='doc/swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),

    path('redoc', TemplateView.as_view(
        template_name='doc/redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),

    path('', include(rest_router.urls)),
    path('', include(users_nested_router.urls)),
]
