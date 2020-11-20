from django.db import models
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField


class CompanyInfo(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    phone = models.CharField(_("Phone number"), max_length=30)
    email = models.EmailField(_("E-mail"),)
    street = models.CharField(_("Street"), max_length=100)
    zip_city = models.CharField(_("Zip Code/City"), max_length=100)
    start_time = models.TimeField(_("Start time"),)
    end_time = models.TimeField(_("End time"),)
    about = RichTextField(verbose_name=_("About"),)
    delivery = RichTextField(verbose_name=_("Delivery"),)
    privacy = RichTextField(verbose_name=_("Privacy"),)
    returns = RichTextField(verbose_name=_("Returns"),)
    contact_us = RichTextField(verbose_name=_("Contact us"),)
    jobs = RichTextField(verbose_name=_("Jobs"),)

    class Meta:
        verbose_name = _("Company information")
        verbose_name_plural = _("Company informations")

    def __str__(self):
        return f"Company {self.name} - Details"
