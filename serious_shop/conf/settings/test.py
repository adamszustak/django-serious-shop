from .base import *
from pathlib import Path

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
