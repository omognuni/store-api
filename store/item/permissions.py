from rest_framework.permissions import BasePermission,SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        '''로그인 안한 경우 Item 목록 읽기만 가능'''
        return request.method in SAFE_METHODS