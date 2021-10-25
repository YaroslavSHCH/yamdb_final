from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from rest_framework import serializers, validators

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        validators=[
            EmailValidator,
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким email уже зарегестрирован'
            )
        ])
    role = serializers.ChoiceField(choices=User.UserRoles.choices())

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        ]
        validators = [
            validators.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email'],
                message='Пользователь с таким email и username уже существует',
            )
        ]
