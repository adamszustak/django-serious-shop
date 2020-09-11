from pathlib import Path
import os
import json

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _


with open("serious_shop/conf/settings/config.json") as config_file:
    secrets = json.load(config_file)


def get_secret(setting, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

MAIN_DIR = Path(__file__).resolve(strict=True).parent.parent.parent


SECRET_KEY = get_secret("SECRET_KEY")


DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "items.apps.ItemsConfig",
    "lib.apps.LibConfig",
    "cart.apps.CartConfig",
    "ckeditor",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "crispy_forms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "conf.urls"

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
                "lib.context_processors.get_section",
                "lib.context_processors.get_company_info",
                "lib.context_processors.get_category",
                "lib.context_processors.cart",
            ],
        },
    },
]
WSGI_APPLICATION = "conf.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_secret("NAME_DB"),
        "USER": get_secret("USER_DB"),
        "PASSWORD": get_secret("PASS_DB"),
        "HOST": "localhost",
        "PORT": "",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


LANGUAGE_CODE = "pl-pl"
LANGUAGES = (
    ("en", _("English")),
    ("pl", _("Polish")),
)
# LOCALE_PATHS = (
#     os.path.join(MAIN_DIR, 'locale'),
# )

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(MAIN_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(MAIN_DIR, "media")

CRISPY_TEMPLATE_PACK = "bootstrap4"

CKEDITOR_CONFIGS = {
    "default": {
        "skin": "moono",
        "toolbar_Full": [
            [
                "Styles",
                "CodeSnippet",
                "Format",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "SpellChecker",
                "Undo",
                "Redo",
            ],
            ["Link", "Unlink"],
            ["Table", "HorizontalRule"],
            ["TextColor", "BGColor"],
            ["Smiley", "SpecialChar"],
            ["Source"],
            ["JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock"],
            ["NumberedList", "BulletedList"],
            ["Indent", "Outdent"],
            ["Maximize"],
        ],
    }
}


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


COMPANY_NAME = "Serious Shop"

CART_SESSION_ID = "cart"
MAX_ITEM_QUANTITY_IN_CART = 10

SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
LOGIN_REDIRECT_URL = "/"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGOUT_ON_GET = True
