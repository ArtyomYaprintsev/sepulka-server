from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from account.models import User


def abstract_validate_user_role(user, role):
    if user.role != role:
        raise ValidationError(
            _("%(username)s is not a %(role)s"),
            params={"username": user.username, "role": role.label,},
        )


def validate_user_shmurdik(value):
    return abstract_validate_user_role(
        value, User.RoleChoice.SHMURDIK,
    )


def validate_user_grymzik(value):
    return abstract_validate_user_role(
        value, User.RoleChoice.GRYMZIK,
    )


def validate_user_fufelnitsa(value):
    return abstract_validate_user_role(
        value, User.RoleChoice.FUFELNITSA,
    )
