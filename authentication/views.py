from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from .models import Confirmation
from .serializers import ConfirmationSerializer, RegistrationSerializer

User = get_user_model()


class EmailSender(viewsets.GenericViewSet, mixins.CreateModelMixin):

    permission_classes = [AllowAny]
    serializer_class = ConfirmationSerializer
    queryset = Confirmation.objects.all()

    def perform_create(self, serializer):
        return serializer.save(
            confirmation_code=Confirmation.generate_confirm_code(),
            user=self.request.user
        )


class TokenAuthorization(viewsets.ModelViewSet):

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
