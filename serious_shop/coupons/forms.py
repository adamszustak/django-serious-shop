from django import forms
from django.utils.translation import ugettext_lazy as _


class CouponForm(forms.Form):
    code = forms.CharField(label=_("Coupon Code"))
