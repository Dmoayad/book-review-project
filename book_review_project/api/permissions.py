# api/permissions.py

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the review.
        return obj.user == request.user


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Allows read-only access for everyone, but write access only for admins.
    """

    def has_permission(self, request, view):
        # Allow read-only methods for all users (authenticated or not)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow write methods only for admin users
        return request.user and request.user.is_staff
