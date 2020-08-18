import pytest

from django.contrib.admin.sites import AdminSite
from django.conf import settings
from django.urls import reverse
from django.contrib.admin.sites import AdminSite

from shop.admin import WearAdmin, ItemAdmin
from shop.models.item import WearProxy, Item, WearSize
from shop.forms import WearSizeForm, WearProxyForm, ItemForm


@pytest.mark.django_db
def test_wearadmin(start_setup, admin_client, request):
    url = reverse('admin:shop_wearproxy_add')
    response = admin_client.get(url)
    sizes = [item[1] for item in WearSize.SIZES]
    assert response.status_code == 200
    assert '<option value="A">Accessories</option>' not in str(response.context['adminform'].form)
    for size in sizes:
        assert size in str(response.context['inline_admin_formset'].formset)
    

    site = AdminSite()
    wear_admin = WearAdmin(WearProxy, site)
    assert 'quantity' not in wear_admin.get_fieldsets(request)[0][1]['fields']
    assert 'add_quantity' not in wear_admin.get_fieldsets(request)[0][1]['fields']
    assert wear_admin.get_queryset(request).count() == 1


@pytest.mark.django_db
def test_itemadmin(start_setup, admin_client, request):
    url = reverse('admin:shop_item_add')
    response = admin_client.get(url)
    assert response.status_code == 200
    assert '<option value="F">Female</option>' not in str(response.context['adminform'].form)
    assert '<option value="M">Male</option>' not in str(response.context['adminform'].form)
    assert WearSize.LARGE in str(response.context['inline_admin_formset'].formset)

    site = AdminSite()
    item_admin = ItemAdmin(Item, site)
    assert item_admin.get_queryset(request).count() == 1