from decimal import Decimal
from unittest.mock import patch

from django.conf import settings
from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.test import Client
from django.urls import resolve, reverse

import braintree
import factory
import pytest
from addresses.forms import BillingAddressForm, ShippingAddressForm
from cart.views import add_to_cart
from items.models import Category, Item
from lib.utils import get_sentinel_user_anonymous
from orders.models import Order, OrderItem
from orders.views import checkout
from payments.tasks import order_confirmation

from .conftest import normalized_data
from .factories import (
    AddressFactory,
    CategoryFactory,
    CompanyFactory,
    ItemAccessoryFactory,
    ItemWearFactory,
    OrderFactory,
    UserFactory,
    WearSizeFactory,
)


@pytest.mark.django_db
def test_item_list_GET(client, base_items):
    ItemAccessoryFactory.create_batch(2)
    url = reverse("items:home")
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["filter"].qs.count() == 4
    assert response.context["slider"] is True

    resolver = resolve("/")
    assert resolver.view_name == "items:home"

    wear, item = base_items
    category = wear.category
    url = reverse("items:category_list_item", kwargs={"path": category.get_path()},)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["filter"].qs.count() == 1
    assert "slider" not in response.context

    resolver = resolve("/category/male/glasses")
    assert resolver.view_name == "items:category_list_item"

    url = reverse("items:search_results")
    response = client.get(url, {"search": "Wear-"})
    assert response.status_code == 200
    assert response.context["filter"].qs.count() == 1

    resolver = resolve("/search/")
    assert resolver.view_name == "items:search_results"


@pytest.mark.django_db
def test_itemdetailview_list_GET(client, base_items):
    wear, item = base_items
    url = reverse("items:detail_item", kwargs={"slug": wear.slug})
    response = client.get(url)
    assert response.status_code == 200

    qs = Item.objects.active()
    assert list(response.context["item_list"]) == list(qs)

    resolver = resolve("/item/pierwszy/")
    assert resolver.view_name == "items:detail_item"


@pytest.mark.django_db
def test_commonview_list_GET(client):
    CompanyFactory()
    generics = ["delivery", "privacy", "returns", " contact_us", " jobs", "about-us"]
    for generic in generics:
        url = reverse("items:generic_info", kwargs={"topic": generic})
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
def test_add_to_cart_POST(base_items, user_client):
    wear, item = base_items
    client = user_client
    url1 = reverse("cart:add_to_cart", kwargs={"item_id": item.id})
    response = client.post(url1)
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

    response = client.post(url1, **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"})
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
    response = client.post(url2)
    session = client.session
    cart = session[settings.CART_SESSION_ID]
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert response.status_code == 302
    assert f'url="/item/{wear.slug}' in str(response)
    assert "You need to choose size" == messages[0]
    assert cart.get(f"{wear.id}-None", None) == None

    url3 = reverse("cart:add_to_cart_size", kwargs={"item_id": wear.id, "size": "M"})
    key2 = f"{wear.id}-M"
    response = client.post(url3)
    session = client.session
    cart = session[settings.CART_SESSION_ID]
    assert response.status_code == 302
    assert 'url="/cart/detail/"' in str(response)
    assert cart.get(key2, None)

    response = client.get(url3)
    assert response.status_code == 302


@pytest.mark.django_db
def test_remove_from_cart_POST(base_items, user_client):
    wear, item = base_items
    url = reverse("cart:add_to_cart", kwargs={"item_id": item.id})
    user_client.post(url)
    response = user_client.post(url, **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"})
    session = user_client.session
    cart = session[settings.CART_SESSION_ID]
    assert response.status_code == 200
    assert cart
    assert cart[f"{item.id}-None"]["quantity"] == 2

    url2 = reverse("cart:remove_one_cart", kwargs={"item_id": item.id, "size": None})
    response = user_client.post(url2, **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"})
    session = user_client.session
    cart = session[settings.CART_SESSION_ID]
    assert response.status_code == 200
    assert cart[f"{item.id}-None"]["quantity"] == 1

    response = user_client.post(url2, **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"})
    session = user_client.session
    cart = session[settings.CART_SESSION_ID]
    assert not cart
    assert response.status_code == 200

    url = reverse("cart:add_to_cart_size", kwargs={"item_id": wear.id, "size": "M"})
    user_client.get(url)
    url3 = reverse("cart:remove_item_cart", kwargs={"item_id": wear.id, "size": "M"})
    response = user_client.post(url3)
    session = user_client.session
    cart = session[settings.CART_SESSION_ID]
    assert not cart
    assert response.status_code == 302


@pytest.mark.django_db
def test_checkout(base_items, user_client, user_user):
    wear, item = base_items
    client = user_client
    user = user_user
    url = reverse("orders:checkout")
    response = client.get(url)
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "Your cart is empty" == messages[0]
    assert response.status_code == 302

    # logged-in user
    url1 = reverse("cart:add_to_cart", kwargs={"item_id": item.id})
    response1 = client.post(url1)
    url2 = reverse("orders:checkout")
    response2 = client.get(url2)
    session = client.session
    cart = session[settings.CART_SESSION_ID]
    assert response2.status_code == 200
    assert response2.context["cart"]
    assert response2.context["total"]

    ## test forms-first creation
    assert response2.context["billing_form"]["address_type"].value() == "billing"
    assert response2.context["shipping_form"]["address_type"].value() == "shipping"
    with pytest.raises(KeyError):
        assert response2.context["shipping_form"]["email"]
    assert response2.context["shipping_form"]["is_default"].value() == False

    billing_data = {"billing-" + x: y for x, y in normalized_data.items()}
    shipping_data = {"shipping-" + x: y for x, y in normalized_data.items()}
    form_billing = BillingAddressForm(data=normalized_data, user=user)
    form_shipping = ShippingAddressForm(data=normalized_data, user=user)
    assert form_billing.is_valid()
    assert form_shipping.is_valid()

    full_data = {**billing_data, **shipping_data}
    response3 = client.post(url2, data=full_data)
    order_qs = Order.objects.filter(user=user, status="created")
    order = order_qs[0]
    shipping_address = [str(x) for x in order.shipping_address.__dict__.values()]
    billing_address = [str(x) for x in order.billing_address.__dict__.values()]
    assert response3.status_code == 302
    assert order_qs.count() == 1
    for value in shipping_data.values():
        assert value in shipping_address
    for value in billing_data.values():
        assert value in billing_address
    assert order.user == user
    assert list(order.items.all()) == list(OrderItem.objects.all())

    # AnonymousUser
    client = Client()
    url1 = reverse("cart:add_to_cart", kwargs={"item_id": item.id})
    response1 = client.post(url1)
    url2 = reverse("orders:checkout")
    response2 = client.get(url2)
    session = client.session
    cart = session[settings.CART_SESSION_ID]
    assert response2.status_code == 200
    assert response2.context["cart"]
    assert response2.context["total"]

    ## test forms
    assert response2.context["billing_form"]["address_type"].value() == "billing"
    assert response2.context["shipping_form"]["address_type"].value() == "shipping"
    with pytest.raises(KeyError):
        assert response2.context["shipping_form"]["is_default"]
    assert response2.context["shipping_form"]["email"]

    response3 = client.post(url2, data=full_data)
    assert response3.status_code == 302
    order_qs = Order.objects.filter(
        user=get_sentinel_user_anonymous(), status="created"
    )
    order = order_qs[0]
    shipping_address = [str(x) for x in order.shipping_address.__dict__.values()]
    billing_address = [str(x) for x in order.billing_address.__dict__.values()]
    assert order_qs.count() == 1
    assert Order.objects.all().count() == 2
    for value in shipping_data.values():
        assert value in shipping_address
    for value in billing_data.values():
        assert value in billing_address
    assert order.user == get_sentinel_user_anonymous()
    assert order.items.all().count() == 1


@pytest.mark.django_db
def test_order_payment_GET(base_items, user_client, user_user):
    gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
    user = user_user
    client = user_client
    order = OrderFactory(user=user)
    url3 = reverse("payments:order_payment", kwargs={"order_id": order.id})
    response = client.get(url3)
    assert response.status_code == 200
    assert response.context["client_token"]

    response = Client().get(url3)
    assert response.status_code == 403


@pytest.mark.django_db
def test_order_payment_POST(base_items, user_client, user_user):
    gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
    user = user_user
    client = user_client
    order = OrderFactory(user=user)
    url3 = reverse("payments:order_payment", kwargs={"order_id": order.id})
    # FAILED
    response = client.post(url3)
    assert response.status_code == 302

    order = Order.objects.get(id=order.id)
    session = client.session
    assert order.status == "unpaid"
    with pytest.raises(KeyError):
        assert session[settings.CART_SESSION_ID]

    ## CELERY TASK
    # result = order_confirmation.delay(order.id, order.status, '/')
    # print(result)
    # ACCEPTED
    result = gateway.transaction.sale(
        {
            "amount": "10.00",
            "payment_method_nonce": "fake-valid-nonce",
            "options": {"submit_for_settlement": True},
        }
    )
    assert result.is_success
