import factory
import pytest
import random
from factory.faker import faker


from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.files import File
from django.template.defaultfilters import slugify

from items.models import Item, Category, ItemImage, WearSize


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


# class OrderItemFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = OrderItem

#     user = factory.SubFactory(UserFactory)
#     item = factory.SubFactory(ItemFactory)
#     size = None


# class OrderFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Order

#     user = factory.SubFactory(UserFactory)
#     ordered_date = FAKE.future_date()
