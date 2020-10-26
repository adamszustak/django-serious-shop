from .base import *

DEBUG = False

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = get_secret("HOST_EMAIL")
EMAIL_USE_SSL = get_secret("SSL_BOOL_EMAIL")
EMAIL_PORT = get_secret("PORT_EMAIL")
EMAIL_HOST_USER = EMAIL
EMAIL_HOST_PASSWORD = get_secret("PASS_EMAIL")
