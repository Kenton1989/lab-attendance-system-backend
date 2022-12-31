from rest_framework.filters import SearchFilter
from .base import BaseModelViewSet
from rest_api.serializers import UserSerializer
from rest_api.models import User
from rest_api.permissions import UserAccessPermission


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = (SearchFilter,)
    search_fields = ('username', 'display_name',)

    permission_classes = (UserAccessPermission, )

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        if pk == 'me':
            self.kwargs['pk'] = self.request.user.id
        return super().get_object()
