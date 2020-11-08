from django import forms

from localflavor.pl.forms import PLPostalCodeField

from .models import Address


class AddressForm(forms.ModelForm):
    zip_code = PLPostalCodeField()

    class Meta:
        model = Address
        exclude = ["user"]
        widgets = {"address_type": forms.HiddenInput()}
        labels = {"is_default": "Set as default"}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if not self.user.is_authenticated:
            del self.fields["is_default"]
        else:
            del self.fields["email"]


class ShippingAddressForm(AddressForm):
    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)
        self.fields["address_type"].initial = "shipping"


class BillingAddressForm(AddressForm):
    def __init__(self, *args, **kwargs):
        super(BillingAddressForm, self).__init__(*args, **kwargs)
        self.fields["address_type"].initial = "billing"
