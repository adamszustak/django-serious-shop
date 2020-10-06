import pytest

from django.contrib.admin.sites import AdminSite
from django.conf import settings
from django.urls import reverse

from items.models import Item, WearSize


@pytest.mark.django_db
def test_itemadmin(start_setup, admin_client, request):
    url = reverse("admin:items_item_add")
    response = admin_client.get(url)
    sizes = [item[1] for item in WearSize.SIZES]
    assert response.status_code == 200
    for size in sizes:
        assert str(size) in str(response.context["inline_admin_formset"].formset)


@pytest.mark.django_db
def test_categoryadmin(start_setup, admin_client, request):
    url = reverse("admin:items_category_changelist")
    response = admin_client.get(url)
    assert response.status_code == 200
    assert (
        "Items in specific category" in response.context["result_headers"][3].values()
    )
