import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from sepulka.validators import (validate_user_fufelnitsa,
                                validate_user_grymzik, validate_user_shmurdik)


class Sepulka(models.Model):
    code = models.UUIDField(
        verbose_name=_("code"),
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )

    name = models.CharField(_("name"), max_length=128, db_index=True)

    is_warm = models.BooleanField(_("is warm"), default=False)
    is_square = models.BooleanField(_("is square"), default=False)
    is_soft = models.BooleanField(_("is soft"), default=False)

    class SizeChoice(models.TextChoices):
        XS = "XS"
        S = "S"
        M = "M"
        L = "L"
        XL = "XL"
        XXL = "XXL"

    size = models.CharField(
        _("size"), max_length=3,
        choices=SizeChoice.choices, default=SizeChoice.M,
    )

    class StateChoice(models.IntegerChoices):
        DELETED = 0, _("deleted")
        CREATED = 1, _("created")
        IN_PROCESS = 2, _("in process")
        PROCESSED = 3, _("processed")
        IN_DELIVERY = 4, _("in delivery")
        COMPLETED = 5, _("completed")

    state = models.PositiveSmallIntegerField(
        _("state"), choices=StateChoice.choices, default=StateChoice.CREATED,
    )

    creator = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT,
        verbose_name=_("user creator"),
        validators=[validate_user_shmurdik,],
    )

    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True)

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

        for model in [Process, Delivery]:
            if hasattr(self, model._meta.model_name):
                continue

            model.objects.create(sepulka=self)

    class Meta:
        verbose_name = _("sepulka")
        verbose_name_plural = _("sepulki")
        ordering = ["-date_created",]

    def safe_delete(self):
        self.state = self.StateChoice.DELETED
        return self.save()


class Process(models.Model):
    sepulka = models.OneToOneField(
        Sepulka, on_delete=models.CASCADE,
        verbose_name=_("sepulka"),
    )

    responsible = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT,
        verbose_name=_("responsible user"), 
        default=None, null=True,
        validators=[validate_user_grymzik,],
    )

    is_vaccinated = models.BooleanField(_("is vaccinated"), default=False)
    is_processed = models.BooleanField(_("is processed"), default=False)

    date_updated = models.DateTimeField(_("date updated"), auto_now=True)

    class Meta:
        verbose_name = _("sepulka process")
        verbose_name_plural = _("sepulka processes")


class Delivery(models.Model):
    sepulka = models.OneToOneField(
        Sepulka, on_delete=models.CASCADE,
        verbose_name=_("sepulka"),
    )

    responsible = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT,
        verbose_name=_("responsible user"), 
        default=None, null=True,
        validators=[validate_user_fufelnitsa,],
    )

    class MethodChoice(models.TextChoices):
        SELF_DELIVERY = "SDEL", _("self delivery")
        ROLL = "ROLL", _("roll")
        AIR_BALLOON = "AIRB", _("air balloon")

    method = models.CharField(
        _("type"), choices=MethodChoice.choices,
        max_length=4, default=None, null=True,
    )

    date_updated = models.DateTimeField(_("date updated"), auto_now=True)

    class Meta:
        verbose_name = _("sepulka delivery")
        verbose_name_plural = _("sepulka deliveries")


class Flow(models.Model):
    sepulka = models.ForeignKey(
        Sepulka, on_delete=models.CASCADE,
        verbose_name=_("sepulka"),
    )

    message = models.CharField(_("message"), max_length=256)

    date_created = models.DateTimeField(_("date created"), auto_now_add=True)

    class Meta:
        verbose_name = _("sepulka flow")
        verbose_name_plural = _("sepulka flows")
