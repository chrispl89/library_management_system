from rest_framework import permissions

class IsLibrarianOrReadOnly(permissions.BasePermission):
    """"
    Allows secure methods (GET, HEAD, OPTIONS) to all logged in,
    but write operations (POST, PUT, PATCH, DELETE) only for users with the 'librarian' role.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.role == "librarian"

class IsAdmin(permissions.BasePermission):
    """
    Allows write operations only for users with the 'admin' role.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == "admin"
