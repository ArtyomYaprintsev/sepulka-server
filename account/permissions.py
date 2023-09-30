from rest_framework.permissions import BasePermission

from account.models import User


class IsShmurdikOrStaffPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and (
                request.user.is_staff
                or request.user.role == User.RoleChoice.SHMURDIK
            )
        )
