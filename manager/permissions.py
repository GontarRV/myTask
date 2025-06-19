from rest_framework import permissions

class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or hasattr(request.user, 'manager')
        )