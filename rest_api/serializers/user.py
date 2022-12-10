from rest_framework import serializers
from django.contrib import auth

User = auth.get_user_model()

# first we define the serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "full_name")

