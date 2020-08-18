import pytest
import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.test.client import Client

from shop.models.company_info import CompanyInfo
from .factories import ItemFactory, WearProxyFactory, UserFactory


@pytest.fixture()
def start_setup(db):
    company = CompanyInfo.objects.create(
        name = settings.COMPANY_NAME,
        phone = '1',
        email = 'mm@wp.pl',
        start_time = datetime.time(10, 33, 45),
        end_time = datetime.time(10, 33, 45),
        about = 'lol',
        delivery = 'lol',
        privacy = 'lol',
        returns = 'lol',
        contact_us = 'lol',
        jobs = 'lol',
    )
    wear = WearProxyFactory(category='M')
    accessory = ItemFactory()
    return wear, accessory


@pytest.fixture()
def admin_user(db, django_user_model, django_username_field): 
    user = UserFactory(email='admin@example.com', password=make_password('secret'),
                       is_active=True, is_staff=True, is_superuser=True)
    return user


@pytest.fixture()
def admin_client(db, admin_user):
    client = Client()
    client.login(username=admin_user.username, password='secret')
    return client