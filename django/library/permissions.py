from rest_framework import permissions

class IsLibrarianOrReadOnly(permissions.BasePermission):
    """
    Only the librarian can edit/delete, the rest can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  
            return True  
        return request.user.is_authenticated and request.user.role == "librarian"

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Only the administrator can edit/delete, the rest have read-only access.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  
        return request.user.is_authenticated and request.user.role == "admin"
