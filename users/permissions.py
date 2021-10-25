from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAllUsersOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated and request.user == obj.author
            or request.user.is_staff or request.user.is_moderator
        )


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_anonymous and request.user.is_moderator


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_anonymous and request.user.is_admin
