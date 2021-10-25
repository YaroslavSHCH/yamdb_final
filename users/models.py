from enum import Enum

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from rest_framework_simplejwt.tokens import AccessToken


class UserManager(BaseUserManager):

    def create_user(self, email, username=None, password=None):

        if email is None:
            raise TypeError('Users must have an email address.')

        data = {
            'email': self.normalize_email(email),
            'username': username
        }

        if not username:
            data['username'] = data['email']

        user = self.model(**data)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.role = User.UserRoles.ADMIN
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):

    class UserRoles(Enum):
        MODERATOR = 'moderator'
        ADMIN = 'admin'
        USER = 'user'

        def __str__(self):
            return str(self.value)

        def __eq__(self, other):
            return str(self.value) == other

        @classmethod
        def choices(cls):
            return tuple((role.value, role.name.lower()) for role in cls)

    username = models.CharField(
        db_index=True, max_length=255, unique=True,
        error_messages={'required': 'Поле должно быть заполнено',
                        'unique': ('Пользователь с таким '
                                   'username уже зарегестрирован')})
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(blank=True, max_length=255)
    last_name = models.CharField(blank=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(choices=UserRoles.choices(),
                            default=UserRoles.USER, max_length=255)

    # Свойство USERNAME_FIELD сообщает нам, какое поле мы будем использовать
    # для входа в систему. В данном случае мы хотим использовать почту.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Сообщает Django, что определенный выше класс UserManager
    # должен управлять объектами этого типа.
    objects = UserManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.email

    @property
    def is_user(self):
        return self.role == self.UserRoles.USER

    @property
    def is_moderator(self):
        return self.role == self.UserRoles.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.UserRoles.ADMIN

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.username

    @property
    def token(self):
        return str(AccessToken.for_user(self))
