import csv
import io

from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.urls import reverse

import pytest
from addresses.admin import AddressAdmin
from items.admin import CategoryAdmin, ItemAdmin
from items.models import Item, WearSize
from orders.admin import OrderAdmin
from orders.models import Order

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
    order = OrderFactory()
    order1 = OrderFactory()
    url = reverse("admin:orders_order_changelist")
    data = {
        "action": "export_to_csv",
        "_selected_action": Order.objects.all().values_list("pk", flat=True),
    }
    response = admin_client.post(url, data, follow=True)
    assert response.status_code == 200

    content = response.content.decode("utf-8")
    cvs_reader = csv.reader(io.StringIO(content))
    body = list(cvs_reader)
    headers = body.pop(0)
    fields = [
        field
        for field in Order._meta.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    for field in fields:
        assert str(field.verbose_name) in str(headers)
    assert str(order.id) and str(order1.id) in str(body)
    assert (
        response["Content-Disposition"]
        == f"attachment; filename=Orders {order1.id}-{order.id}.csv"
    )
