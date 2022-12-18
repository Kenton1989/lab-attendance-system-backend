from rest_framework.viewsets import ModelViewSet
from rest_api.serializers import CourseSerializer
from rest_api.models import Course


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
