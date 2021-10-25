from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import permissions
from .serializers import UserSerializer

User = get_user_model()


class UsersView(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAdmin]
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(detail=False, permission_classes=[IsAuthenticated],
            methods=['get', 'patch'], url_path='me')
    def me(self, request):
        user = get_object_or_404(User, id=self.request.user.id)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
