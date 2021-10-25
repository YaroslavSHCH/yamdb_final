from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from rest_framework import serializers

from .models import Confirmation
from .utils import send_confirm_code

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    # Убедитесь, что пароль содержит не менее 8 символов, не более 128,
    # и так же что он не может быть прочитан клиентской стороной

    # Клиентская сторона не должна иметь возможность отправлять токен вместе с
    # запросом на регистрацию. Сделаем его доступным только на чтение.
    token = serializers.CharField(max_length=255, read_only=True)
    email = serializers.EmailField(write_only=True)
    confirmation_code = serializers.CharField(
        min_length=8,
        max_length=128,
        write_only=True
    )

    class Meta:
        model = User
        # Перечислить все поля, которые могут быть включены в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = ['email', 'token', 'confirmation_code']
        extra_kwargs = {'email': {'validators': [EmailValidator]}}

    def validate(self, data):
        is_active_code = Confirmation.objects.filter(
            email=data['email'], confirmation_code=data['confirmation_code']
        )
        if not is_active_code.exists():
            raise serializers.ValidationError(
                'Указаны невалидные данные для авторизации'
            )
        return data

    def create(self, validated_data):
        user = User.objects.filter(email=validated_data['email'])

        if not user.exists():
            return User.objects.create_user(email=validated_data['email'])
        return user.first()

    def save(self, **kwargs):
        # Код подтверждения больше не нужен, освобождаем БД после использования
        Confirmation.objects.filter(
            email=self.validated_data['email'],
            confirmation_code=self.validated_data['confirmation_code']
        ).delete()
        return super().save(**kwargs)


class ConfirmationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    confirmation_code = serializers.ReadOnlyField()

    class Meta:
        model = Confirmation
        fields = ['email', 'confirmation_code']

    def save(self, **kwargs):
        email = self.validated_data.get('email')
        confirmation_code = kwargs.get('confirmation_code')

        send_confirm_code(email, confirmation_code)

    def validate_email(self, value):
        # Если в базе есть уже отправленный код, то удалим его
        Confirmation.objects.filter(email=value).delete()

        return value
