from django.core.exceptions import PermissionDenied
from .models import Order


def user_is_order_author(function):
    def wrap(request, *args, **kwargs):
        order = Order.objects.get(id=kwargs["order_id"])
        if order.user == request.user or request.session.session_key == order.session:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
