from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.urls import reverse

import pytest
from addresses.admin import AddressAdmin
from items.models import Item, WearSize

from .factories import (
    AddressFactory,
    CompanyFactory,
    OrderFactory,
    OrderItemFactory,
)


@pytest.mark.django_db
def test_itemadmin(admin_client, request):
    url = reverse("admin:items_item_add")
    response = admin_client.get(url)
    sizes = [item[1] for item in WearSize.SIZES]
    assert response.status_code == 200
    for size in sizes:
        assert str(size) in str(response.context["inline_admin_formset"].formset)


@pytest.mark.django_db
def test_categoryadmin(admin_client, request):
    url = reverse("admin:items_category_changelist")
    response = admin_client.get(url)
    assert response.status_code == 200
    assert (
        "Items in specific category" in response.context["result_headers"][3].values()
    )


@pytest.mark.django_db
def test_addressadmin(admin_client, request):
    url = reverse("admin:addresses_address_add")
    response = admin_client.get(url)
    address = AddressFactory()
    OrderFactory(shipping_address=address)
    OrderFactory(billing_address=address)
    admin_function_result = AddressAdmin.order_ids(AddressAdmin, obj=address)
    assert response.status_code == 200
    assert admin_function_result == "1,2"
