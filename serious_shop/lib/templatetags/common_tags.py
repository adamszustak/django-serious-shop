from django import template

from shop.models.item import SubCategory


register = template.Library()


@register.simple_tag
def in_cat(category):
    return SubCategory.objects.filter(item__category=category).distinct()
