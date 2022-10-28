from rest_framework.permissions import BasePermission


class IsAdminOrCRUOnly(BasePermission):
    '''관리자 외 로그인한 이용자는 Create, Read, Update만 가능'''
    def has_permission(self, request, view):
        if view.action in ['create', 'retrieve', 'update', 'partial_update', 'list'] and request.user.is_authenticated:
            return True
        if view.action == 'destroy' and request.user.is_staff:
            return True
        return False