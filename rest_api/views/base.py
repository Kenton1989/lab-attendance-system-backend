from rest_framework.viewsets import ModelViewSet
from rest_api.permissions import ExtendedObjectPermission


class BaseModelViewSet(ModelViewSet):
    def perform_create(self, serializer):
        self.check_create_object_permissions(self, self.request, serializer)
        return super().perform_create(serializer)

    def check_create_object_permissions(self, request, serializer):
        for perm in self.get_permissions():
            if not isinstance(perm, ExtendedObjectPermission):
                continue

            if perm.has_create_object_permission(request.user, request, self, serializer):
                self.permission_denied(
                    request,
                    message=getattr(perm, 'message', None),
                    code=getattr(perm, 'code', None)
                )
