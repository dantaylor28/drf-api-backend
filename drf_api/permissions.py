from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsAdminOrReadOnly(permissions.IsAdminUser):
    """
    Custom permission to ensure only the admin can have access to
    certain features, primarily creating and editing categories
    """
    def has_permission(self, request, view):
        is_admin = super(
            IsAdminOrReadOnly,
            self).has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin
