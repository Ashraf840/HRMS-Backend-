from rest_framework import permissions

# Custom Account Edit Permission Classes
from rest_framework.permissions import SAFE_METHODS

import UserApp.models


class Authenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.email_validated)


class EmployeeAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.email_validated and request.user.is_employee)


class IsHrOrReadOnly(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.email_validated
            and request.user.is_hr or request.user.is_authenticated and request.user.is_employee
            and request.user.email_validated and request.method in SAFE_METHODS
        )


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


class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to Admin users.
    like CEO, GM , HR,
    """
    message = 'You are not authorised to view this page.'

    def has_permission(self, request, view):
        permission = False
        designation = UserApp.models.EmployeeInfoModel.objects.get(user_id=request.user).designation.designation
        if designation == 'CEO' or designation == 'GM' or designation == 'HR' or designation == 'PM':
            permission = True
        return bool((request.user and request.user.is_hr) or permission)


class IsEmployee(permissions.BasePermission):
    """
    Allows access only to Admin users.
    like CEO, GM , HR,
    """
    message = 'You are not authorised to view this page.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_employee)


class IsCandidateUser(permissions.BasePermission):
    """
    Allows access only to Candidate users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_candidate)


class IsAuthor(permissions.BasePermission):
    """
       Allows access only to Author.
       """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return obj.user == request.user
