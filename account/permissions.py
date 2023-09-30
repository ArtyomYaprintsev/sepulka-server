from rest_framework.permissions import BasePermission

from account.models import User


class AbstractUserRolePermission(BasePermission):
    allowed_role = None

    def check_user_instance(self, user):
        return user.role == self.allowed_role

    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated
            and self.check_user_instance(request.user)
        )


class CheckUserIsStaffMixin(AbstractUserRolePermission):
    def check_user_instance(self, user):
        return user.is_staff or super().check_user_instance(user)


class IsShmurdikPermission(AbstractUserRolePermission):
    allowed_role = User.RoleChoice.SHMURDIK


class IsGrymzikPermission(AbstractUserRolePermission):
    allowed_role = User.RoleChoice.GRYMZIK


class IsFufelnitsaPermission(AbstractUserRolePermission):
    allowed_role = User.RoleChoice.FUFELNITSA


class IsShmurdikOrStaffPermission(
    CheckUserIsStaffMixin,
    IsShmurdikPermission,
):
    pass
