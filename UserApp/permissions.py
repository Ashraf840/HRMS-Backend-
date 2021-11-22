from rest_framework import permissions


# Custom Account Edit Permission Classes

class EditPermission(permissions.BasePermission):
    message = 'You are not authorize to edit this page'

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.user == request.user


class IsHrUser(permissions.BasePermission):
    """
    Allows access only to HR users.
    """
    message = 'You are not authorised to view this page.'
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_hr)


class IsCandidateUser(permissions.BasePermission):
    """
    Allows access only to Candidate users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_candidate)
