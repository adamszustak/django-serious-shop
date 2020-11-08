from pathlib import Path

import braintree

from .base import *

MAIN_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:",}}

DEBUG = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [MAIN_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "lib.context_processors.get_category",
                "lib.context_processors.cart",
            ],
        },
    },
]

BRAINTREE_MERCHANT_ID = get_secret("BRAINTREE_MERCHANT_ID")
BRAINTREE_PUBLIC_KEY = get_secret("BRAINTREE_PUBLIC_KEY")
BRAINTREE_PRIVATE_KEY = get_secret("BRAINTREE_PRIVATE_KEY")

BRAINTREE_CONF = braintree.Configuration(
    braintree.Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY,
)

CELERY_ALWAYS_EAGER = True
TEST_RUNNER = "djcelery.contrib.test_runner.CeleryTestSuiteRunner"
