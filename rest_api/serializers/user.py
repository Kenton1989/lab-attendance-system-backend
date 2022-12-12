from rest_framework import serializers
from rest_api.models import User
from django.contrib.auth.password_validation import validate_password

# first we define the serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'email',
                  'display_name', 'is_active')

    def create(self, validated_data):
        user: User = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user: User = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user
