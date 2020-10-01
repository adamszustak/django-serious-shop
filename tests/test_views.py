import pytest

from django.urls import reverse, resolve
from django.conf import settings
from django.db import IntegrityError
from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist

from items.models import Category, Item, Section
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
def test_sectionlistitemview__GET(start_setup, client, base_items):
    wear, item, category = base_items
    url = reverse(
        "items:section_category_list_item",
        kwargs={"section": "male", "slug": category.slug},
    )
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["object_list"].count() == 1
    assert "slider" not in response.context

    url2 = reverse("items:section_list_item", kwargs={"section": "male"})
    response2 = client.get(url2)
    assert response2.status_code == 200
    assert response2.context["object_list"].count() == 1
    assert "slider" not in response.context

    resolver = resolve("/section/male/")
    resolver1 = resolve("/section/male/glasses")
    assert resolver.view_name == "items:section_list_item"
    assert resolver1.view_name == "items:section_category_list_item"


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
    wear, item, category = base_items
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
def test_cart_logged_GET(client, start_setup, base_items, user_client):
    wear, item, category = base_items
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
        "price": str(item.actual_price),
        "size": None,
    }

    response = client.get(url1)
    session = client.session
    cart = session[settings.CART_SESSION_ID]
    assert response.status_code == 200
    assert cart[key] == {
        "quantity": 2,
        "price": str(item.actual_price),
        "size": None,
    }


# @pytest.mark.django_db
# def test_add_to_cart_GET(start_setup, user_client, user_user, cart_helper, client):
#     item1, wear_size, item2 = cart_helper
#     url1 = reverse("items:add_to_cart", kwargs={"slug": item1.slug})
#     response = user_client.get(url1)
#     messages = [m.message for m in get_messages(response.wsgi_request)]
#     assert response.status_code == 302
#     assert "You have to choose size" == messages[0]
#     with pytest.raises(ObjectDoesNotExist):
#         assert not OrderItem.objects.get(user=user_user, ordered=False, item=item1)

#     url2 = reverse(
#         "items:add_to_cart_size", kwargs={"slug": item1.slug, "size": wear_size.size}
#     )
#     response = user_client.get(url2)
#     messages = [m.message for m in get_messages(response.wsgi_request)]
#     order_item = OrderItem.objects.get(user=user_user, ordered=False, item=item1)
#     order = Order.objects.get(user=user_user)
#     assert "Item has been added to cart" == messages[1]
#     assert item1 == order_item.item
#     assert order_item.quantity == 1
#     assert order_item in order.items.all()

#     response = user_client.get(url2)
#     messages = [m.message for m in get_messages(response.wsgi_request)]
#     order_item = OrderItem.objects.get(user=user_user, ordered=False, item=item1)
#     assert response.status_code == 302
#     assert "Item quantity has been updated" == messages[2]
#     assert order_item.quantity == 2
#     assert order.items.count() == 1

#     url3 = reverse("items:add_to_cart", kwargs={"slug": item2.slug})
#     response = user_client.get(url3)
#     messages = [m.message for m in get_messages(response.wsgi_request)]
#     order = Order.objects.get(user=user_user)
#     assert response.status_code == 302
#     assert "This item has been added" == messages[3]
#     assert order.items.count() == 2


# @pytest.mark.django_db
# def test_remove_from_cart_GET(start_setup, user_client, user_user, cart_helper, client):
#     item1, wear_size, item2 = cart_helper
#     url = reverse("items:add_to_cart", kwargs={"slug": item2.slug})
#     user_client.get(url)
#     user_client.get(url)
#     assert (
#         OrderItem.objects.get(user=user_user, ordered=False, item=item2).quantity == 2
#     )
#     url = reverse("items:remove_one_cart", kwargs={"slug": item2.slug})
#     response = user_client.get(url)
#     order_item = OrderItem.objects.get(user=user_user, ordered=False, item=item2)
#     messages = [m.message for m in get_messages(response.wsgi_request)]
#     assert response.status_code == 302
#     assert order_item.quantity == 1

#     response = user_client.get(url)
#     assert response.status_code == 302
#     with pytest.raises(ObjectDoesNotExist):
#         assert not OrderItem.objects.get(user=user_user, ordered=False, item=item2)
#     with pytest.raises(ObjectDoesNotExist):
#         assert not Order.objects.get(user=user_user, ordered=False)

#     url2 = reverse(
#         "items:add_to_cart_size", kwargs={"slug": item1.slug, "size": wear_size.size}
#     )
#     user_client.get(url2)
#     user_client.get(url2)
#     assert (
#         OrderItem.objects.get(user=user_user, ordered=False, item=item1).quantity == 2
#     )
#     url2 = reverse(
#         "items:remove_item_from_cart_size",
#         kwargs={"slug": item1.slug, "size": wear_size.size},
#     )
#     response = user_client.get(url2)
#     assert response.status_code == 302
#     with pytest.raises(ObjectDoesNotExist):
#         assert not OrderItem.objects.get(user=user_user, ordered=False, item=item1)
