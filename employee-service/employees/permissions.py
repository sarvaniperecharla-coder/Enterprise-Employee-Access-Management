from rest_framework.permissions import BasePermission


class IsManager(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and hasattr(request.user, "employee_profile")
            and request.user.employee_profile.role == "Manager"
        )



class IsHR(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and hasattr(request.user, "employee_profile")
            and request.user.employee_profile.role == "HR"
        )