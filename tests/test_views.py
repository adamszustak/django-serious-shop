import pytest
from decimal import Decimal

from django.urls import reverse, resolve
from django.conf import settings
from django.db import IntegrityError
from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist

from items.models import Category, Item
from .factories import (
    ItemAccessoryFactory,
    WearSizeFactory,
    ItemWearFactory,
    CategoryFactory,
)


@pytest.mark.django_db
def test_homeview_list_GET(start_setup, client):
    ItemAccessoryFactory.create_batch(2)
    url = reverse("items:home")
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["object_list"].count() == 2
    assert response.context["slider"] is True

    resolver = resolve("/")
    assert resolver.view_name == "items:home"


@pytest.mark.django_db
def test_categoryview__GET(start_setup, client, base_items):
    wear, item = base_items
    category = wear.category
    url = reverse("items:category_list_item", kwargs={"path": category.get_path()},)
    response = client.get(url)
    assert response.status_code == 200
    assert "slider" not in response.context

    resolver = resolve("/category/male/glasses")
    assert resolver.view_name == "items:category_list_item"


@pytest.mark.django_db
def test_searchresultview_list_GET(start_setup, client, base_items):
    url = reverse("items:search_results")
    response = client.get(url, {"search": "Wear-"})
    assert response.status_code == 200
    assert response.context["object_list"].count() == 1

    resolver = resolve("/search/")
    assert resolver.view_name == "items:search_results"


@pytest.mark.django_db
def test_itemdetailview_list_GET(start_setup, client, base_items):
    wear, item = base_items
    url = reverse("items:detail_item", kwargs={"slug": wear.slug})
    response = client.get(url)
    assert response.status_code == 200

    qs = Item.objects.active()
    assert list(response.context["item_list"]) == list(qs)

    resolver = resolve("/item/pierwszy/")
    assert resolver.view_name == "items:detail_item"


@pytest.mark.django_db
def test_commonview_list_GET(start_setup, client):
    generics = ["delivery", "privacy", "returns", " contact_us", " jobs", "about-us"]
    for generic in generics:
        url = reverse("items:generic_info", kwargs={"topic": generic})
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
def test_add_to_cart_GET(start_setup, base_items, user_client):
    wear, item = base_items
    client = user_client
    url1 = reverse("cart:add_to_cart", kwargs={"item_id": item.id})
    response = client.get(url1)
    session = client.session
    cart = session[settings.CART_SESSION_ID]
    assert response.status_code == 302
    assert cart

    item_id = str(item.id)
    key = f"{item_id}-None"
    assert cart[key] == {
        "quantity": 1,
        "price": f"{item.actual_price:.2f}",
        "size": None,
    }

    response = client.get(url1)
    session = client.session
    cart = session[settings.CART_SESSION_ID]
    assert response.status_code == 200
    assert cart[key] == {
        "quantity": 2,
        "price": f"{item.actual_price:.2f}",
        "size": None,
    }
    assert list(response.json()["cart"].keys()) == [key]
    assert Decimal(response.json()["item_final_price"]) == Decimal(
        item.actual_price * 2
    )
    assert int(response.json()["len_cart"]) == 2
    assert Decimal(response.json()["final_price"]) == Decimal(item.actual_price * 2)

    url2 = reverse("cart:add_to_cart", kwargs={"item_id": wear.id})
    response = client.get(url2)
    session = client.session
    cart = session[settings.CART_SESSION_ID]
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert response.status_code == 302
    assert f'url="/item/{wear.slug}' in str(response)
    assert "You need to choose size" == messages[0]
    assert cart.get(f"{wear.id}-None", None) == None

    url3 = reverse("cart:add_to_cart_size", kwargs={"item_id": wear.id, "size": "M"})
    key2 = f"{wear.id}-M"
    response = client.get(url3)
    session = client.session
    cart = session[settings.CART_SESSION_ID]
    assert response.status_code == 302
    assert 'url="/cart/detail/"' in str(response)
    assert cart.get(key2, None)


@pytest.mark.django_db
def test_remove_from_cart_GET(start_setup, base_items, user_client):
    wear, item = base_items
    url = reverse("cart:add_to_cart", kwargs={"item_id": item.id})
    user_client.get(url)
    response = user_client.get(url)
    session = user_client.session
    cart = session[settings.CART_SESSION_ID]
    assert response.status_code == 200
    assert cart
    assert cart[f"{item.id}-None"]["quantity"] == 2

    url2 = reverse("cart:remove_one_cart", kwargs={"item_id": item.id, "size": None})
    response = user_client.get(url2)
    session = user_client.session
    cart = session[settings.CART_SESSION_ID]
    assert response.status_code == 200
    assert cart[f"{item.id}-None"]["quantity"] == 1

    response = user_client.get(url2)
    session = user_client.session
    cart = session[settings.CART_SESSION_ID]
    assert not cart
    assert response.status_code == 200

    url = reverse("cart:add_to_cart_size", kwargs={"item_id": wear.id, "size": "M"})
    user_client.get(url)
    url3 = reverse("cart:remove_item_cart", kwargs={"item_id": wear.id, "size": "M"})
    response = user_client.get(url3)
    session = user_client.session
    cart = session[settings.CART_SESSION_ID]
    assert not cart
    assert response.status_code == 302
