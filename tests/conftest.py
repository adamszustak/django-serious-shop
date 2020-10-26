import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.shortcuts import reverse
from django.test.client import Client

import pytest
from lib.models import CompanyInfo

from .factories import (
    CategoryFactory,
    ItemAccessoryFactory,
    ItemWearFactory,
    UserFactory,
    WearSizeFactory,
)


@pytest.fixture()
def base_items(db):
    category_wear = CategoryFactory(name="trousers", need_sizes=True)
    category_item = CategoryFactory(name="glasses")
    wear = ItemWearFactory(category=category_wear)
    item = ItemAccessoryFactory(category=category_item)
    wear_size = WearSizeFactory(item=wear, size="M", quantity=10)
    return wear, item


@pytest.fixture()
def admin_user(db, django_user_model, django_username_field):
    user = UserFactory(
        email="admin@example.com",
        password=make_password("secret"),
        is_active=True,
        is_staff=True,
        is_superuser=True,
    )
    return user


@pytest.fixture()
def admin_client(db, admin_user):
    client = Client()
    client.login(username=admin_user.username, password="secret")
    return client


@pytest.fixture
def user_user(db, django_user_model, django_username_field):
    user = UserFactory(
        username="user",
        password=make_password("secret"),
        first_name="Normal",
        last_name="User",
        is_active=True,
    )
    return user


@pytest.fixture()
def user_client(db, user_user):
    client = Client()
    client.login(username=user_user.username, password="secret")
    return client
