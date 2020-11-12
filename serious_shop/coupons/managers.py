from django.apps import apps
from django.db import models


class CouponQuerySet(models.query.QuerySet):
    def are_valid(self):
        model = apps.get_model("coupons", "Coupon")
        active = [coupon.id for coupon in model.objects.all() if coupon.is_valid()]
        return model.objects.filter(id__in=active)
