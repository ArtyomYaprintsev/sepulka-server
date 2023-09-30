from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = None
    last_name = None

    class RoleChoice(models.IntegerChoices):
        FUFELNITSA = 0, _("fufelnitsa")
        GRYMZIK = 1, _("grymzik")
        SHMURDIK = 2, _("shmurdik")

    role = models.PositiveSmallIntegerField(
        _("role"), choices=RoleChoice.choices, default=RoleChoice.FUFELNITSA,
    )
