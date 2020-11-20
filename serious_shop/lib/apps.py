from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LibConfig(AppConfig):
    name = "lib"
    verbose_name = _("Company info")
