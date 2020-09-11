from django.db import models
from django.db.models import Q


class CategoryManager(models.Manager):
    def in_section(self, section):
        return self.filter(items__section=section, items__active=True).distinct()


class ItemQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (
            Q(title__icontains=query)
            | Q(category__name__icontains=query)
            | Q(color__icontains=query)
        )
        return self.filter(lookups)

    def in_section(self, section):
        return self.filter(section=section)

    def in_category(self, section, category):
        return self.filter(section=section, category__slug=category)


class ItemManager(models.Manager):
    def get_queryset(self):
        return ItemQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def search(self, query):
        return self.get_queryset().active().search(query)

    def in_section(self, section):
        return self.get_queryset().active().in_section(section)

    def in_category(self, section, category):
        return self.get_queryset().active().in_category(section, category)
