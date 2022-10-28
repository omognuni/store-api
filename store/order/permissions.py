from rest_framework.permissions import BasePermission


class IsAdminOrCRUOnly(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'retrieve', 'update', 'partial_update', 'list'] and request.user.is_authenticated:
            return True
        if view.action == 'destroy' and request.user.is_staff:
            return True
        return False