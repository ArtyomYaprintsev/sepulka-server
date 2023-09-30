from rest_framework.permissions import BasePermission

from account.models import User


class AbstractUserRolePermission(BasePermission):
    """Allow access by the give `allowed_role` field.

    If the given user is authenticated calls checks from the
    `check_user_instance` method.

    """

    allowed_role = None
    """Specified allowed `user.role` field."""

    def check_user_instance(self, user):
        """Check that the given user role and `allowed_role` are equal."""
        return user.role == self.allowed_role

    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated
            and self.check_user_instance(request.user)
        )


class CheckUserIsStaffMixin(AbstractUserRolePermission):
    """Provide additional user is staff check.
    
    Overrides `check_user_instance` method.
    """

    def check_user_instance(self, user):
        return user.is_staff or super().check_user_instance(user)


class IsShmurdikPermission(AbstractUserRolePermission):
    """Allow access for `SHMURDIK` users."""

    allowed_role = User.RoleChoice.SHMURDIK


class IsGrymzikPermission(AbstractUserRolePermission):
    """Allow access for `GRYMZIK` users."""

    allowed_role = User.RoleChoice.GRYMZIK


class IsFufelnitsaPermission(AbstractUserRolePermission):
    """Allow access for `FUFELNITSA` users."""

    allowed_role = User.RoleChoice.FUFELNITSA


class IsShmurdikOrStaffPermission(
    CheckUserIsStaffMixin,
    IsShmurdikPermission,
):
    """Allow access for `SHMURDIK` of staff users."""
