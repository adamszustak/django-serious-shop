import pytest

from django.urls import reverse, resolve
from django.conf import settings
from django.db import IntegrityError
from django.contrib.messages import get_messages

from shop.models.item import Category, Item
from .factories import (
    ItemFactory,
    WearProxyFactory,
    WearSizeFactory,
    OrderFactory,
    OrderItemFactory,
)


@pytest.mark.django_db
def test_homeview_list_GET(start_setup, client):
    url = reverse("shop:home")
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["object_list"].count() == 2
    assert response.context["slider"] is True

    resolver = resolve("/")
    assert resolver.view_name == "shop:home"


@pytest.mark.django_db
def test_sectionlistitemview__GET(start_setup, client):
    WearProxyFactory(category="M", subcategory__name="glasses")
    ItemFactory(category="A", subcategory__name="glasses")
    url = reverse(
        "shop:category-subcategory-list-item",
        kwargs={"category": "male", "subcategory": "glasses"},
    )
    url1 = reverse(
        "shop:category-subcategory-list-item",
        kwargs={"category": "male", "subcategory": "glasses"},
    )
    response = client.get(url)
    response1 = client.get(url1)
    assert response.context["object_list"].count() == 1
    assert response1.context["object_list"].count() == 1

    url2 = reverse("shop:category-list-item", kwargs={"category": "male"})
    response2 = client.get(url2)
    assert response2.status_code == 200
    assert response2.context["object_list"].count() == 2

    resolver = resolve("/section/male/")
    resolver1 = resolve("/section/male/glasses")
    assert resolver.view_name == "shop:category-list-item"
    assert resolver1.view_name == "shop:category-subcategory-list-item"


@pytest.mark.django_db
def test_searchresultview_list_GET(start_setup, client):
    url = reverse("shop:search-results")
    response = client.get(url, {"search": "Product_W"})
    assert response.status_code == 200
    assert response.context["object_list"].count() == 1

    resolver = resolve("/search/")
    assert resolver.view_name == "shop:search-results"


@pytest.mark.django_db
def test_itemdetailview_list_GET(start_setup, client):
    wear, accessory = start_setup
    url = reverse("shop:detail-item", kwargs={"slug": wear.slug})
    response = client.get(url)
    assert response.status_code == 200

    qs = Item.objects.all()
    assert list(response.context["item_list"]) == list(qs)

    resolver = resolve("/item/pierwszy/")
    assert resolver.view_name == "shop:detail-item"


@pytest.mark.django_db
def test_commonview_list_GET(start_setup, client):
    generics = ["delivery", "privacy", "returns", " contact_us", " jobs", "about-us"]
    for generic in generics:
        url = reverse("shop:generic-info", kwargs={"topic": generic})
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
def test_add_to_cart_GET(start_setup, user_client, client):
    item1 = ItemFactory(quantity=5, price=25.00, discount_price=10.00)
    item1.sizes.add(WearSizeFactory(item=item1, size="M", quantity=10))
    url = reverse("shop:add-to-cart", kwargs={"slug": item1.slug})
    response = user_client.get(url)
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert response.status_code == 302
    assert "Item has been added to cart" in messages
    assert len(messages) == 1


# ........
