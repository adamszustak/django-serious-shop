import itertools

from django.db import models
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey

from .managers import ItemManager
from lib.utils import image_directory_path


class Category(MPTTModel):
    name = models.CharField(_("Name"), max_length=30)
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
        db_index=True,
        verbose_name=_("Parent"),
    )
    need_sizes = models.BooleanField(_("Need sizes"), default=False)
    slug = models.SlugField()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        unique_together = (
            "parent",
            "slug",
        )
        ordering = ["tree_id", "lft"]

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return f"{self.name} - {self.parent}"

    def get_absolute_url(self):
        return reverse("items:category_list_item", kwargs={"path": self.get_path()})


class Item(models.Model):
    category = TreeForeignKey(
        "items.Category",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Category"),
        null=True,
        blank=True,
    )
    title = models.CharField(_("Title"), max_length=50)
    price = models.DecimalField(_("Price"), max_digits=5, decimal_places=2, default=0)
    discount_price = models.DecimalField(
        _("Discount price"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    description = RichTextField(_("Description"))
    color = models.CharField(_("Color"), max_length=10, blank=True)
    quantity = models.IntegerField(_("Item quantity"), default=0, null=True, blank=True)
    slug = models.SlugField(editable=False)
    mod_date = models.DateTimeField(_("Updated at"), auto_now=True)
    created_date = models.DateTimeField(_("Created at"), auto_now_add=True)
    active = models.BooleanField(_("Active"), default=False)

    objects = ItemManager()

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

    def __str__(self):
        return self.title

    def clean(self):
        if self.category.need_sizes:
            if self.quantity > 0:
                raise ValidationError(_("Quantity must be set with size!"))

    def _generate_slug(self):
        value = self.title
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not self.__class__.objects.filter(
                category=self.category, slug=slug_candidate
            ).exists():
                break
            slug_candidate = f"{slug_original}-{i}"
        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("items:detail_item", kwargs={"slug": self.slug})

    def get_main_photo(self):
        try:
            return self.images.first().image
        except AttributeError:
            return None

    @property
    def actual_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price


class WearSize(models.Model):
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"
    XLARGE = "XL"
    XXLARGE = "XXL"
    SIZES = [
        (SMALL, _("Small")),
        (MEDIUM, _("Medium")),
        (LARGE, _("Large")),
        (XLARGE, _("X Large")),
        (XXLARGE, _("XX Large")),
    ]
    item = models.ForeignKey(
        "items.Item",
        on_delete=models.CASCADE,
        related_name="sizes",
        blank=True,
        null=True,
        verbose_name=_("Item"),
    )
    size = models.CharField(_("Size"), max_length=3, choices=SIZES)
    quantity = models.IntegerField(_("Size quantity"),)

    class Meta:
        unique_together = (("item", "size"),)
        ordering = ["item__title"]

    def __str__(self):
        return f"{self.item.title} - {self.size}"

    def clean(self):
        if not self.item.category.need_sizes:
            raise ValidationError("Size is for clothes only!")


class ItemImage(models.Model):
    item = models.ForeignKey(
        "items.Item",
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
        verbose_name=_("Item"),
    )
    image = models.ImageField(_("Image"), upload_to=image_directory_path)

    def __str__(self):
        return f"{self.item.title} - {self.image.name}"
