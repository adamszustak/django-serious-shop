import factory
import pytest
import random
from factory.faker import faker


from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.files import File

from shop.models.item import WearSize, WearProxy, Item, Category, SubCategory, ItemImage


FAKE = faker.Faker()


class SubCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubCategory
    
    name = factory.Sequence(lambda n: 'subcategory%d' % n)


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    category = Category.ACCESSORY
    title = "Product_I-" + FAKE.name()
    subcategory = factory.SubFactory(SubCategoryFactory)
    price = FAKE.pydecimal(positive=True, left_digits=3, right_digits=2)
    discount_price = FAKE.pydecimal(positive=True, left_digits=2, right_digits=2)
    description = factory.Faker('text')
    created_date = factory.LazyFunction(timezone.now)
    quantity = FAKE.pyint(max_value=50)
    add_quantity = None


class WearSizeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WearSize
    
    item = None
    size = factory.Iterator(WearSize.SIZES, getter=lambda c: c[0])
    quantity = FAKE.pyint(max_value=50)
    add_quantity = 0


class WearProxyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WearProxy

    category = factory.Iterator([item for item in Category.choices if item[0]==Category.FEMALE or item[0]==Category.MALE], getter=lambda c: c[0])
    title = "Product_W-" + FAKE.name()
    subcategory = factory.SubFactory(SubCategoryFactory)
    price = FAKE.pydecimal(positive=True, left_digits=3, right_digits=2)
    discount_price = FAKE.pydecimal(positive=True, left_digits=2, right_digits=2)
    description = factory.Faker('text')
    created_date = factory.LazyFunction(timezone.now)
    size = factory.RelatedFactory(WearSizeFactory, factory_related_name='item', size='L', quantity=10)
    quantity = None
    add_quantity = None


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
    
    username = factory.Sequence(lambda n: 'user-%d' % n)
    password = 'secret'
