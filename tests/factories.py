import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.template.defaultfilters import slugify
from django.utils import timezone

import factory
import pytest
from addresses.models import Address
from factory.faker import faker
from items.models import Category, Item, ItemImage, WearSize
from lib.models import CompanyInfo
from orders.models import Order, OrderItem

FAKE = faker.Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: "category%d" % n)
    slug = factory.LazyAttribute(lambda a: slugify(a.name))
    parent = None


class ItemAccessoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    title = "Product_Acc-" + FAKE.name()
    category = factory.SubFactory(CategoryFactory)
    price = FAKE.pydecimal(positive=True, left_digits=3, right_digits=2)
    discount_price = FAKE.pydecimal(positive=True, left_digits=2, right_digits=2)
    description = factory.Faker("text")
    created_date = factory.LazyFunction(timezone.now)
    active = True
    quantity = FAKE.pyint(max_value=50)


class WearSizeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WearSize

    item = None
    size = factory.Iterator(WearSize.SIZES, getter=lambda c: c[0])
    quantity = FAKE.pyint(max_value=50)


class ItemWearFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    title = "Product_Wear-" + FAKE.name()
    category = factory.SubFactory(CategoryFactory)
    price = FAKE.pydecimal(positive=True, left_digits=3, right_digits=2)
    discount_price = FAKE.pydecimal(positive=True, left_digits=2, right_digits=2)
    description = factory.Faker("text")
    created_date = factory.LazyFunction(timezone.now)
    size = factory.RelatedFactory(
        WearSizeFactory, factory_related_name="item", size="L", quantity=10
    )
    active = True


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: "user-%d" % n)
    password = "secret"


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    address_type = factory.Iterator(Address.ADDRESS_TYPE, getter=lambda c: c[0])
    first_name = FAKE.first_name()
    last_name = FAKE.last_name()
    email = FAKE.email()
    street = FAKE.street_name()
    flat_nr = FAKE.building_number()
    zip_code = "05-482"
    city = FAKE.city()
    province = "mazowieckie"
    is_default = False


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    shipping_address = factory.SubFactory(AddressFactory)
    billing_address = factory.SubFactory(AddressFactory)
    created_date = FAKE.date_time()
    updated_date = FAKE.date_time()


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    item = factory.SubFactory(ItemWearFactory)
    size = factory.Iterator(WearSize.SIZES, getter=lambda c: c[0])
    price = FAKE.pydecimal(positive=True, left_digits=3, right_digits=2)
    quantity = FAKE.pyint(max_value=50)


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CompanyInfo

    name = settings.COMPANY_NAME
    phone = FAKE.phone_number()
    email = FAKE.email()
    start_time = FAKE.time()
    end_time = FAKE.time()
    about = factory.Faker("text")
    delivery = factory.Faker("text")
    privacy = factory.Faker("text")
    returns = factory.Faker("text")
    contact_us = factory.Faker("text")
    jobs = factory.Faker("text")
