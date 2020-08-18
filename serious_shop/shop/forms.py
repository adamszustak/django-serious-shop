from django import forms

from .models.item import WearSize, Item, Category, WearProxy


class WearSizeForm(forms.ModelForm):
    class Meta:
        model = WearSize
        fields = [
            "size",
            "add_quantity",
            "quantity",
        ]

    def __init__(self, *args, **kwargs):
        if "instance" not in kwargs:
            initial = kwargs.get("initial", {})
            sizes = [size[0] for size in WearSize.SIZES]
            for num, size in enumerate(sizes):
                if kwargs.get("prefix") == f"sizes-{num}":
                    initial["size"] = sizes[num]
            kwargs["initial"] = initial
        super(WearSizeForm, self).__init__(*args, **kwargs)

    def has_changed(self):
        return True


class WearProxyForm(forms.ModelForm):
    class Meta:
        model = WearProxy
        exclude = []

    def __init__(self, *args, **kwargs):
        super(WearProxyForm, self).__init__(*args, **kwargs)
        choices = [
            item
            for item in Category.choices
            if item[0] == Category.FEMALE or item[0] == Category.MALE
        ]
        self.fields["category"].choices = choices


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        choices = [item for item in Category.choices if item[0] == Category.ACCESSORY]
        self.fields["category"].choices = choices
