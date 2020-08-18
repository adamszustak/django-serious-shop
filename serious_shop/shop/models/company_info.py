from ckeditor.fields import RichTextField

from django.db import models


class CompanyInfo(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    about = RichTextField()
    delivery = RichTextField()
    privacy = RichTextField()
    returns = RichTextField()
    contact_us = RichTextField()
    jobs = RichTextField()

    def __str__(self):
        return f"Company {self.name} - Details"
