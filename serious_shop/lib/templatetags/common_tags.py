from django import template

from items.models import Category

register = template.Library()


@register.simple_tag
def in_cat(category):
    """
    Checks wheter given category is in section
    """
    return Category.objects.in_section(category)
