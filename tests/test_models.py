import pytest

from django.urls import reverse, resolve
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from items.models import Item, Category, ItemImage
from lib.utils import image_directory_path
from .factories import (
    ItemAccessoryFactory,
    ItemWearFactory,
    WearSizeFactory,
    CategoryFactory,
)


@pytest.mark.django_db
def test_category_model(start_setup):
    base_cat = CategoryFactory()
    category1 = CategoryFactory(name="wear", parent=base_cat)
    item1 = ItemAccessoryFactory(category=category1)
    assert Category.objects.count() == 2
    assert category1.items.count() == 1
    assert list(category1.items.all()) == [item1]

    item2 = ItemAccessoryFactory(category=category1)
    assert category1.items.count() == 2
    assert list(category1.items.all()) == [item1, item2]
    assert base_cat.items.count() == 0


@pytest.mark.django_db
def test_item_model(start_setup):
    category_wear = CategoryFactory(need_sizes=True)
    category_item = CategoryFactory(need_sizes=False)
    item2 = ItemAccessoryFactory(
        title="same_title", price=10.00, discount_price=5.00, category=category_item
    )
    item3 = ItemAccessoryFactory(
        title="same_title", price=10.00, discount_price=None, category=category_item
    )
    wear1 = ItemWearFactory(title="same_title", category=category_wear, color="Blue")
    wear2 = ItemWearFactory(title="same_title", category=category_wear, color="Blue")
    assert item2.slug == "same_title"
    assert item3.slug == "same_title-1"
    assert wear1.slug == "same_title"
    assert wear2.slug == "same_title-1"
    assert item2.actual_price == 5.00
    assert item3.actual_price == 10.00

    wear1.quantity = 10
    with pytest.raises(ValidationError):
        assert wear1.full_clean()

    item2.active = False
    item2.save()
    assert Item.objects.active().count() == 3
    assert list(Item.objects.active()) == [item3, wear1, wear2]
    assert Item.objects.search(wear1.color).count() == 2
    assert list(Item.objects.search(wear1.color)) == [wear1, wear2]
    assert Item.objects.in_category(category_wear).count() == 2
    assert Item.objects.in_category(category_item).count() == 1
    assert list(Item.objects.in_category(category_wear)) == [wear1, wear2]


@pytest.mark.django_db
def test_wearsize_model(start_setup):
    category_wear = CategoryFactory(need_sizes=True)
    wear1 = ItemWearFactory(category=category_wear)
    item1 = ItemAccessoryFactory()
    wearsize1 = WearSizeFactory(size="M", quantity=10)
    wearsize1.item = item1
    with pytest.raises(ValidationError):
        assert wearsize1.full_clean()

    wear1.sizes.add(wearsize1)
    assert wear1.sizes.all().count() == 2

    with pytest.raises(Exception):
        assert wearsize1.save()


# @pytest.mark.django_db
# def test_orderitem_model(start_setup):
#     item1 = ItemFactory(quantity=5, price=25.00, discount_price=10.00)
#     item1.sizes.add(WearSizeFactory(item=item1, size="M", quantity=10))
#     order_item1 = OrderItemFactory(
#         item=item1, size=item1.sizes.first().size, quantity=5
#     )
#     assert order_item1.get_total_item_price == 125
#     assert order_item1.get_total_discount_item_price == 50
#     assert order_item1.get_amount_saved == 75
#     assert order_item1.get_final_price == 50


# @pytest.mark.django_db
# def test_order_model(start_setup):
#     item1 = ItemFactory(quantity=5, price=25.00, discount_price=10.00)
#     item2 = ItemFactory(quantity=10, price=50.00, discount_price=25.00)
#     item1.sizes.add(WearSizeFactory(item=item1, size="M", quantity=10))
#     order_item1 = OrderItemFactory(
#         item=item1, size=item1.sizes.first().size, quantity=5
#     )
#     order_item2 = OrderItemFactory(item=item2)
#     order = OrderFactory()
#     order.items.add(order_item1, order_item2)
#     assert order.get_total == 75
#     assert order.items_quantity == 6
