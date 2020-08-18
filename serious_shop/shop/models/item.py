import itertools
from ckeditor.fields import RichTextField

from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from lib.utils import image_directory_path


class Category(models.TextChoices):
    FEMALE = "F", "Female"
    MALE = "M", "Male"
    ACCESSORY = "A", "Accessories"


class SubCategory(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sub-categories"


class Item(models.Model):
    category = models.CharField(max_length=2, choices=Category.choices)
    title = models.CharField(max_length=50)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    description = RichTextField()
    color = models.CharField(max_length=10, blank=True)
    quantity = models.IntegerField(
        verbose_name="item quantity", default=0, null=True, blank=True
    )
    add_quantity = models.IntegerField(default=0, null=True, blank=True)
    slug = models.SlugField(editable=False)
    mod_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Accessory Item"
        verbose_name_plural = "Accessories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:detail-item", kwargs={"slug": self.slug})

    def _generate_slug(self):
        value = self.title
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not self.__class__.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = f"{slug_original}-{i}"
        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        if self.add_quantity:
            self.quantity += self.add_quantity
            self.add_quantity = 0
        super().save(*args, **kwargs)

    def get_main_photo(self):
        try:
            return self.images.first().image.url
        except AttributeError:
            return None


class WearProxy(Item):
    class Meta:
        proxy = True
        verbose_name = "Wear Item"


class WearSize(models.Model):
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"
    XLARGE = "XL"
    XXLARGE = "XXL"
    SIZES = [
        (SMALL, "Small"),
        (MEDIUM, "Medium"),
        (LARGE, "Large"),
        (XLARGE, "X Large"),
        (XXLARGE, "XX Large"),
    ]
    item = models.ForeignKey(
        "Item", on_delete=models.CASCADE, related_name="sizes", blank=True, null=True
    )
    size = models.CharField(max_length=3, choices=SIZES)
    quantity = models.IntegerField(verbose_name="item quantity", default=0)
    add_quantity = models.IntegerField(blank=True, default=0)

    class Meta:
        unique_together = (("item", "size"),)

    def __str__(self):
        return f"{self.item.title} - {self.size}"

    def save(self, *args, **kwargs):
        if self.add_quantity:
            self.quantity += self.add_quantity
            self.add_quantity = 0
        super(WearSize, self).save(*args, **kwargs)


class ItemImage(models.Model):
    item = models.ForeignKey(
        "Item", on_delete=models.CASCADE, related_name="images", null=True, blank=True
    )
    image = models.ImageField(upload_to=image_directory_path)

    def __str__(self):
        return f"{self.image.name}"
