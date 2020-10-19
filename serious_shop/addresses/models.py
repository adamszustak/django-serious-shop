from localflavor.pl.pl_administrativeunits import (
    ADMINISTRATIVE_UNIT_CHOICES as provinces,
)

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import transaction

from lib.utils import get_sentinel_user_deleted, get_sentinel_user_anonymous
from .managers import AddressQuerySet


class Address(models.Model):
    BILLING_ADDRESS = "billing"
    SHIPPING_ADDRESS = "shipping"
    ADDRESS_TYPE = [
        (BILLING_ADDRESS, _("Billing address")),
        (SHIPPING_ADDRESS, _("Shipping address")),
    ]
    address_type = models.CharField(
        _("Address type"), max_length=30, choices=ADDRESS_TYPE
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET(get_sentinel_user_deleted),
        related_name=("addresses"),
        verbose_name=_("User"),
        blank=True,
        null=True,
        default=get_sentinel_user_anonymous,
    )
    first_name = models.CharField(_("First name"), max_length=50)
    last_name = models.CharField(_("Last name"), max_length=50)
    email = models.EmailField()
    street = models.CharField(_("Street"), max_length=50)
    flat_nr = models.IntegerField(_("Flat number"))
    zip_code = models.CharField(_("zip code"), max_length=20)
    city = models.CharField(_("City"), max_length=50)
    province = models.CharField(_("Province"), max_length=50, choices=provinces)
    is_default = models.BooleanField(default=False)

    objects = AddressQuerySet.as_manager()

    def __str__(self):
        return f"{self.city} {self.street} {self.flat_nr}"

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    @transaction.atomic
    def save(self, *args, **kwargs):
        default_shipping = type(self).objects.default_shipping(self.user)
        default_billing = type(self).objects.default_billing(self.user)
        if not default_billing.exists() or not default_shipping.exists():
            if self.user == get_sentinel_user_anonymous():
                pass
            else:
                self.is_default = True
        if (self.is_default and default_billing.exists()) or (
            self.is_default and default_shipping.exists()
        ):
            if self.id:
                pass
            elif self.address_type == "billing":
                default_billing.update(is_default=False)
            else:
                default_shipping.update(is_default=False)
        super(Address, self).save(*args, **kwargs)

    def get_short(self):
        return f"{self.first_name} {self.last_name}, {self.province} {self.city} {self.zip_code} {self.street}/{self.flat_nr}"
