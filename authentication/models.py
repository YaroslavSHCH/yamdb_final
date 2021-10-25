import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

User = get_user_model()


class Confirmation(models.Model):

    email = models.EmailField(unique=True)
    confirmation_code = models.TextField(
        validators=[MinLengthValidator(limit_value=8)],
        max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(fields=['email', 'confirmation_code'],
                                    name='unique_email_code')
        ]

    def __str__(self):
        return self.email

    @staticmethod
    def generate_confirm_code():
        return uuid.uuid4().hex
