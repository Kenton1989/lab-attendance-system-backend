from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_api.serializers import UserSerializer
from rest_api.models import User
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = (SearchFilter,)
    search_fields = ('username', 'display_name',)

    @action(detail=False,
            methods=('get', 'patch', 'put'),
            permission_classes=(IsAuthenticated,))
    def me(self, request: Request, *args, **kwargs):
        pk = request.user.id
        self.kwargs['pk'] = pk

        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        elif request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)
        elif request.method == 'PUT':
            return self.update(request, *args, **kwargs)
