from django import forms

from .models import WearSize, Item, Category


class WearSizeForm(forms.ModelForm):
    """
    Form created for adminform, it prepares all fields for given SIZES as initial fields
    """

    class Meta:
        model = WearSize
        fields = [
            "size",
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
