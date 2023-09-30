from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """The user specified by the service conditions represented by this model.

    The model is inherited from `django.contrib.auth.models.AbstractUser` model
    without `first_name` and `last_name` fields. Provides additional `role` char
    field with a choice from `RoleChoice` (`RoleChoice.FUFELNITSA` by default).

    """

    first_name = None
    last_name = None

    class RoleChoice(models.IntegerChoices):
        FUFELNITSA = 0, _("fufelnitsa")
        GRYMZIK = 1, _("grymzik")
        SHMURDIK = 2, _("shmurdik")

    role = models.PositiveSmallIntegerField(
        _("role"), choices=RoleChoice.choices, default=RoleChoice.FUFELNITSA,
    )
