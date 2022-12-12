from django.urls import path, include
from rest_api.views.user import UserList, UserDetails
from rest_api.views import token, WeekViewSet
from rest_framework.routers import SimpleRouter

rest_router = SimpleRouter()
rest_router.register(r'weeks', WeekViewSet)

urlpatterns = [
    # authentication API
    path('tokens/', token.CreateToken.as_view()),
    path('tokens/current/', token.RevokeToken.as_view()),
    path('tokens/all/', token.RevokeAllToken.as_view()),

    path('users/', UserList.as_view()),
    path('users/<pk>/', UserDetails.as_view()),

    path('settings/', include('dbsettings.urls')),

    path('', include(rest_router.urls)),
]
