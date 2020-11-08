from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, get_object_or_404, render
from django.template.loader import render_to_string
from django.views.generic import ListView

import weasyprint
from lib.models import CompanyInfo
from orders.models import Order


class OrderUserList(LoginRequiredMixin, ListView):
    model = Order
    template_name = "user_history.html"

    def get_queryset(self):
        user = self.request.user
        return Order.objects.search_by_user(user)


def pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    company = CompanyInfo.objects.latest("id")
    html = render_to_string("pdf.html", {"order": order, "company": company})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=order {order.id}.pdf"
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + "/css/pdf.css")]
    )
    return response
