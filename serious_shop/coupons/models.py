from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from .managers import CouponQuerySet


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    active = models.BooleanField()

    objects = CouponQuerySet.as_manager()

    def __str__(self):
        return f"{self.code}"

    def is_valid(self):
        return self.valid_to > timezone.now()

    @property
    def get_image(self):
        return settings.STATIC_URL + "img/percent.png"
