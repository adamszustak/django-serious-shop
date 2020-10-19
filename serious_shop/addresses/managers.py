from django.db import models


class AddressQuerySet(models.query.QuerySet):
    def default_billing(self, user):
        return self.filter(address_type="billing", is_default=True, user=user)

    def default_shipping(self, user):
        return self.filter(address_type="shipping", is_default=True, user=user)
