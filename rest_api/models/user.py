from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import UserManager

from rest_api.validators import username_validator


class User(AbstractBaseUser, PermissionsMixin):
    '''Customized User class
    https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#auth-custom-user

    It is almost the same to the default User object (django.contrib.auth.models.User).
    Difference includes:
    - first_name & last_name field are replaced with a display_name field.
    - username only allows alphabets and digits.
    '''

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters and digits only.',
        validators=[username_validator],
        error_messages={
            'unique': 'A user with that username already exists.',
        }
    )

    # profile data
    display_name = models.CharField('display name', max_length=150, null=True)

    # profile data required by Django's default admin page,
    # including is_staff, is_active, is_superuser, last_login and date_joined
    email = models.EmailField('email address', null=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into the Django admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.',
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'display_name']

    objects = UserManager()

    def get_full_name(self) -> str:
        return self.display_name

    def get_short_name(self) -> str:
        return self.display_name
