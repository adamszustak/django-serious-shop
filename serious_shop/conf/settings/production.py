import braintree

from .base import *

DEBUG = False

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = get_secret("HOST_EMAIL")
EMAIL_USE_TSL = get_secret("TSL_BOOL_EMAIL")
EMAIL_PORT = get_secret("PORT_EMAIL")
EMAIL_HOST_USER = EMAIL
EMAIL_HOST_PASSWORD = get_secret("PASS_EMAIL")

BRAINTREE_MERCHANT_ID = get_secret("BRAINTREE_MERCHANT_ID")
BRAINTREE_PUBLIC_KEY = get_secret("BRAINTREE_PUBLIC_KEY")
BRAINTREE_PRIVATE_KEY = get_secret("BRAINTREE_PRIVATE_KEY")

BRAINTREE_CONF = braintree.Configuration(
    braintree.Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY,
)
