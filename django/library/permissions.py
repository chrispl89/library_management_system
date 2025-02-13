from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    Odczyt jest dozwolony dla każdego (SAFE_METHODS).
    """

    def has_object_permission(self, request, view, obj):
        # Odczyt (GET, HEAD, OPTIONS) – zawsze dozwolony
        if request.method in permissions.SAFE_METHODS:
            return True

        # Zapis (POST, PUT, PATCH, DELETE) – tylko właściciel może modyfikować
        return obj.added_by == request.user
