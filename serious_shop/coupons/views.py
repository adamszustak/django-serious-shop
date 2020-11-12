from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from cart.cart import Cart

from .forms import CouponForm
from .models import Coupon


@require_POST
def coupon_apply(request):
    form = CouponForm(request.POST)
    if form.is_valid():
        response_data = {}
        try:
            code = request.POST.get("code")
            coupon = Coupon.objects.are_valid().get(code__iexact=code, active=True)
            request.session["coupon_id"] = coupon.id
            cart = Cart(request)
            response_data["code"] = coupon.code
            response_data["discount"] = coupon.discount
            response_data["image"] = coupon.get_image
            response_data["get_discount"] = cart.get_discount()
            response_data["get_total"] = cart.get_final_price()
            response_data["get_final_price"] = cart.get_final_discount_price()
            return JsonResponse(response_data, status=200)
        except ObjectDoesNotExist:
            request.session["coupon_id"] = None
            return JsonResponse({"error": ""}, status=400)
    return JsonResponse({"error": ""}, status=400)


@require_POST
def coupon_delete(request):
    del request.session["coupon_id"]
    return redirect("orders:checkout")
