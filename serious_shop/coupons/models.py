from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .managers import CouponQuerySet


class Coupon(models.Model):
    code = models.CharField(_("Code"), max_length=50, unique=True)
    valid_from = models.DateTimeField(_("Valid from"))
    valid_to = models.DateTimeField(_("Valid to"))
    discount = models.IntegerField(
        _("Discount"), validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    active = models.BooleanField(_("Active"))

    objects = CouponQuerySet.as_manager()

    class Meta:
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")

    def __str__(self):
        return f"{self.code}"

    def is_valid(self):
        return self.valid_to > timezone.now()

    @property
    def get_image(self):
        return settings.STATIC_URL + "img/percent.png"
