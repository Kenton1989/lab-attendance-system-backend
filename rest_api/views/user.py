from rest_framework.viewsets import ModelViewSet
from rest_api.serializers import UserSerializer
from rest_framework.decorators import action
from rest_api.models import User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False,
            methods=['get', 'patch', 'put'],
            permission_classes=[IsAuthenticated])
    def me(self, request: Request, *args, **kwargs):
        pk = request.user.id
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs, pk=pk)
        elif request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs, pk=pk)
        elif request.method == 'PUT':
            return self.update(request, *args, **kwargs, pk=pk)
