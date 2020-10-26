from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField


class CompanyInfo(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    phone = models.CharField(_("Phone number"), max_length=30)
    email = models.EmailField(_("E-mail"),)
    start_time = models.TimeField(_("Start time"),)
    end_time = models.TimeField(_("End time"),)
    about = RichTextField(verbose_name=_("About"),)
    delivery = RichTextField(verbose_name=_("Delivery"),)
    privacy = RichTextField(verbose_name=_("Privacy"),)
    returns = RichTextField(verbose_name=_("Returns"),)
    contact_us = RichTextField(verbose_name=_("Contact us"),)
    jobs = RichTextField(verbose_name=_("Jobs"),)

    def __str__(self):
        return f"Company {self.name} - Details"