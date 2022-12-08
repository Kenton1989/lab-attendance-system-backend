from django.urls import path, include
from .views.user import UserList, UserDetails, GroupList
from .views import token

urlpatterns = [
    # authentication API
    path('tokens/', token.CreateToken.as_view()),
    path('tokens/current/', token.RevokeToken.as_view()),
    path('tokens/all/', token.RevokeAllToken.as_view()),

    path('users/', UserList.as_view()),
    path('users/<pk>/', UserDetails.as_view()),
    path('groups/', GroupList.as_view()),
]
