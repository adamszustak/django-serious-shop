from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.urls import reverse

import pytest
from addresses.admin import AddressAdmin
from items.admin import CategoryAdmin, ItemAdmin
from items.models import Item, WearSize
from orders.admin import OrderAdmin

from .factories import (
    AddressFactory,
    CategoryFactory,
    CompanyFactory,
    ItemWearFactory,
    OrderFactory,
    OrderItemFactory,
)


@pytest.mark.django_db
def test_categoryadmin(admin_client, request):
    url = reverse("admin:items_item_add")
    response = admin_client.get(url)
    category = CategoryFactory()
    ItemWearFactory(category=category)
    category_modeladmin = CategoryAdmin(category, AdminSite())
    admin_function_result = category_modeladmin.view_items_link(category)
    assert response.status_code == 200
    assert (
        admin_function_result
        == '<a href="/admin/items/item/?category__id=1">1 Items</a>'
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


@pytest.mark.django_db
def test_orderadmin(admin_client, request):
    url = reverse("admin:orders_order_add")
    response = admin_client.get(url)
    order = OrderFactory()
    order_modeladmin = OrderAdmin(order, AdminSite())
    assert response.status_code == 200
