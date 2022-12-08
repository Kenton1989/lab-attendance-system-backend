from knox.views import LoginView, LogoutView, LogoutAllView
from rest_framework import views


class CreateToken(LoginView):
    pass


class RevokeToken(views.APIView):
    authentication_classes = LogoutView.authentication_classes
    permission_classes = LogoutView.permission_classes

    knox_logout = LogoutView()

    def delete(self, request, *args, **kwargs):
        return self.knox_logout.post(request, *args, **kwargs)


class RevokeAllToken(views.APIView):
    authentication_classes = LogoutAllView.authentication_classes
    permission_classes = LogoutAllView.permission_classes

    knox_logout_all = LogoutAllView()

    def delete(self, request, *args, **kwargs):
        return self.knox_logout_all.post(request, *args, **kwargs)