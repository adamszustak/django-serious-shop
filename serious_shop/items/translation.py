from modeltranslation.translator import TranslationOptions, register

from .models import Category, Item


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ("name",)


@register(Item)
class ItemTranslation(TranslationOptions):
    fields = (
        "description",
        "color",
    )
