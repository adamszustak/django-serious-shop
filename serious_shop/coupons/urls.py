from django.urls import path

from .views import coupon_apply, coupon_delete

app_name = "coupons"

urlpatterns = [
    path("apply/", coupon_apply, name="apply"),
    path("delete/", coupon_delete, name="delete"),
]
