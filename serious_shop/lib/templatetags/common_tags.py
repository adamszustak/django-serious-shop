from django import template

from items.models import Category

register = template.Library()


@register.simple_tag
def in_cat(category):
    return Category.objects.in_section(category)
