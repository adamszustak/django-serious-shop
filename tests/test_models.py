import pytest

from django.urls import reverse, resolve
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from items.models import Section, Item, Category
from lib.utils import image_directory_path
from .factories import (
    ItemAccessoryFactory,
    ItemWearFactory,
    WearSizeFactory,
    CategoryFactory,
)


@pytest.mark.django_db
def test_category_model(start_setup):
    category = CategoryFactory()
    item2 = ItemAccessoryFactory(category=category, section=Section.MALE)
    item3 = ItemAccessoryFactory()
    assert Category.objects.in_section(section=Section.MALE).count() == 1
    assert list(Category.objects.in_section(section=Section.MALE)) == [category]

    category1 = CategoryFactory()
    item3.category, item3.section = category1, Section.MALE
    item2.save()
    item3.save()
    assert Category.objects.in_section(section=Section.MALE).count() == 2
    assert list(Category.objects.in_section(section=Section.MALE)) == [
        category,
        category1,
    ]


@pytest.mark.django_db
def test_item_model(start_setup):
    category = CategoryFactory()
    item2 = ItemAccessoryFactory(
        title="same_title", price=10.00, discount_price=5.00, category=category
    )
    item3 = ItemAccessoryFactory(title="same_title", price=10.00, discount_price=None)
    wear1 = ItemWearFactory(title="same_title", category=category, color="Blue")
    wear2 = ItemWearFactory(title="same_title", color="Blue")
    assert item2.slug == "same_title"
    assert item3.slug == "same_title-1"
    assert wear1.slug == "same_title-2"
    assert wear2.slug == "same_title-3"
    assert wear1.is_wear == True
    assert item2.is_wear == False
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
    assert Item.objects.in_section(Section.ACCESSORY).count() == 1
    assert list(Item.objects.in_section(Section.ACCESSORY)) == [item3]
    assert Item.objects.in_section(Section.FEMALE).count() == 1
    assert list(Item.objects.in_section(Section.FEMALE)) == [wear1]
    assert Item.objects.in_category(Section.ACCESSORY, category).count() == 0
    assert Item.objects.in_category(Section.FEMALE, category).count() == 1
    assert list(Item.objects.in_category(Section.FEMALE, category)) == [wear1]


@pytest.mark.django_db
def test_wearsize_model(start_setup):
    wear1 = ItemWearFactory()
    item1 = ItemAccessoryFactory()
    wearsize1 = WearSizeFactory(size="M", quantity=10)
    wearsize1.item = item1
    with pytest.raises(ValidationError):
        assert wearsize1.full_clean()

    wear1.sizes.add(wearsize1)
    assert wear1.sizes.all().count() == 2

    with pytest.raises(Exception):
        assert wearsize1.save()


# @pytest.mark.django_db(transaction=True)
# def test_wearproxy_model(start_setup):
#     wear = WearProxyFactory()
#     WearSizeFactory(item=wear, size="M", quantity=10)
#     with pytest.raises(IntegrityError):
#         WearSizeFactory(item=wear, size="M", quantity=10)

#     wearsize_m = wear.sizes.filter(size="M")[0]
#     wearsize_m.add_quantity = 23
#     wearsize_m.save()

#     assert wearsize_m.quantity == 33
#     assert wearsize_m.add_quantity == 0


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
