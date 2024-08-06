from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        user = request.user
        return user.groups.first().name == 'super_admin'