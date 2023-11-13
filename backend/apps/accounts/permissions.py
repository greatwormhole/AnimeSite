from rest_framework.permissions import BasePermission

class IsCurrentUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj == request.user