import pytest

from django.urls import reverse,resolve
from django.conf import settings
from django.db import IntegrityError

from shop.models.item import Category
from .factories import ItemFactory, WearProxyFactory, WearSizeFactory


@pytest.mark.django_db
def test_item_model(start_setup):
    item = ItemFactory(title='same_title')
    item_quantity_before = item.quantity
    item_slug_before = item.slug
    item.add_quantity = 10
    item.save()
    assert item.slug == item_slug_before
    assert item_quantity_before + 10 == item.quantity
    assert item.add_quantity == 0

    item2 = ItemFactory(title='same_title')
    item3 = ItemFactory(title='same_title')
    wear1 = ItemFactory(title='same_title')

    assert item2.slug == 'same_title-1'
    assert item3.slug == 'same_title-2'
    assert wear1.slug == 'same_title-3'


@pytest.mark.django_db(transaction=True)
def test_wearproxy_model(start_setup):
    wear = WearProxyFactory()
    WearSizeFactory(item=wear, size='M', quantity=10)

    with pytest.raises(IntegrityError):
        WearSizeFactory(item=wear, size='M', quantity=10)

    wearsize_m = wear.sizes.filter(size='M')[0]
    wearsize_m.add_quantity = 23
    wearsize_m.save()

    assert wearsize_m.quantity == 33
    assert wearsize_m.add_quantity == 0

