import pytest
import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.test.client import Client
from django.shortcuts import reverse

from lib.models import CompanyInfo
from items.models import Section
from .factories import (
    ItemWearFactory,
    ItemAccessoryFactory,
    UserFactory,
    CategoryFactory,
    WearSizeFactory,
)


@pytest.fixture()
def start_setup(db):
    company = CompanyInfo.objects.create(
        name=settings.COMPANY_NAME,
        phone="1",
        email="mm@wp.pl",
        start_time=datetime.time(10, 33, 45),
        end_time=datetime.time(10, 33, 45),
        about="lol",
        delivery="lol",
        privacy="lol",
        returns="lol",
        contact_us="lol",
        jobs="lol",
    )


@pytest.fixture()
def base_items(db):
    category = CategoryFactory(name="glasses")
    wear = ItemWearFactory(section=Section.MALE, category=category)
    item = ItemAccessoryFactory(category=category)
    wear_size = WearSizeFactory(item=wear, size="M", quantity=10)
    return wear, item, category


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
