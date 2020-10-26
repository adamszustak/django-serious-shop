import braintree

from .base import *

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = [
    "127.0.0.1",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

BRAINTREE_MERCHANT_ID = get_secret("BRAINTREE_MERCHANT_ID")
BRAINTREE_PUBLIC_KEY = get_secret("BRAINTREE_PUBLIC_KEY")
BRAINTREE_PRIVATE_KEY = get_secret("BRAINTREE_PRIVATE_KEY")

BRAINTREE_CONF = braintree.Configuration(
    braintree.Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY,
)
